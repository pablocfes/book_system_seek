from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from books.models import books_collection
from books.api.serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class BookView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Obtiene una lista de libros filtrados por los parámetros de consulta.",
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_QUERY, description="Filtra por título del libro", type=openapi.TYPE_STRING),
            openapi.Parameter('author', openapi.IN_QUERY, description="Filtra por autor del libro", type=openapi.TYPE_STRING),
            openapi.Parameter('published_date', openapi.IN_QUERY, description="Filtra por fecha de publicación", type=openapi.TYPE_STRING),
            openapi.Parameter('genre', openapi.IN_QUERY, description="Filtra por género del libro", type=openapi.TYPE_STRING),
            openapi.Parameter('price', openapi.IN_QUERY, description="Filtra por precio del libro", type=openapi.TYPE_NUMBER),
            openapi.Parameter('page', openapi.IN_QUERY, description="Número de página para la paginación", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Número de resultados por página", type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: openapi.Response(
                description="Lista de libros filtrados y paginados",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_books': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'page': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'page_size': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_pages': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'books': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT)),
                    }
                )
            ),
            404: "No se encontraron libros con los filtros proporcionados",
        }
    )
    def get(self, request):
        try:
            # Filtrar libros por los query_params
            filters = {}
            for param in ['title', 'author', 'published_date', 'genre', 'price']:
                value = request.query_params.get(param)
                if value:
                    # Utilizamos regex para buscar en la cadena de texto sin importar mayúsculas
                    filters[param] = {"$regex": value, "$options": "i"}

            books = list(books_collection.find(filters, {"_id": 0}))

            if not books:
                return Response({"message": "No books found"}, status=status.HTTP_404_NOT_FOUND)

            # Paginación, tomamos los valores de page y page_size de los query_params o usamos valores por defecto
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 10))

            start = (page - 1) * page_size
            end = start + page_size

            paginated_books = books[start:end]

            return Response({
                "total_books": len(books),
                "page": page,
                "page_size": page_size,
                "total_pages": (len(books) + page_size - 1) // page_size,
                "books": paginated_books,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Crea un nuevo libro en la base de datos.",
        request_body=BookSerializer,
        responses={
            201: "Libro creado exitosamente",
            400: "Errores de validación de los datos enviados",
            200: "El libro ya existe en la base de datos",
        }
    )
    def post(self, request):
        try:
            serializer = BookSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data

                # Buscar si ya existe un registro con el mismo título para evitar duplicados
                existing_book = books_collection.find_one({"title": validated_data["title"]})

                if existing_book:
                    # Convertir ObjectId a string para poder ser serializado
                    existing_book["_id"] = str(existing_book["_id"])
                    return Response(existing_book, status=status.HTTP_200_OK)

                # Si no existe, crear uno nuevo
                inserted_id = books_collection.insert_one(validated_data).inserted_id
                validated_data["_id"] = str(inserted_id)  # Agregar el ID al resultado

                return Response(validated_data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Actualiza la información de un libro utilizando el título como referencia.",
        request_body=BookSerializer,
        responses={
            200: "Libro actualizado exitosamente",
            400: "El título es obligatorio para la actualización",
            404: "No se encontró el libro a actualizar",
        }
    )
    def patch(self, request):
        try:
            title = request.data.get('title')
            if not title:
                return Response({"error": "Title is required for updating a book"}, status=status.HTTP_400_BAD_REQUEST)

            book_data = request.data
            result = books_collection.update_one(
                {"title": title},
                {"$set": book_data}
            )
            if result.matched_count == 0:
                return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Book updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Elimina un libro utilizando el título como referencia.",
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description="Título del libro a eliminar")
        }),
        responses={
            200: "Libro eliminado exitosamente",
            400: "El título es obligatorio para eliminar el libro",
            404: "No se encontró el libro a eliminar",
        }
    )
    def delete(self, request):
        try:
            title = request.data.get('title')
            if not title:
                return Response({"error": "Title is required for deleting a book"}, status=status.HTTP_400_BAD_REQUEST)

            result = books_collection.delete_one({"title": title})
            if result.deleted_count == 0:
                return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Book deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AveragePriceView(APIView):
    def get(self, request):
        year = request.query_params.get('year')
        pipeline = [
            {"$match": {"published_date": {"$regex": f"^{year}"}}},
            {"$group": {"_id": None, "average_price": {"$avg": "$price"}}}
        ]
        result = list(books_collection.aggregate(pipeline))
        if result:
            return Response({"average_price": result[0]["average_price"]})
        return Response({"average_price": 0})
