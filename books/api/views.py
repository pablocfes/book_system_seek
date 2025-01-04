from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from books.models import books_collection
from books.api.serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class BookView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Filtrar libros por los query_params
        filters = {}
        for param in ['title', 'author', 'published_date', 'genre', 'price']:
            value = request.query_params.get(param)
            if value:
                filters[param] = {"$regex": value, "$options": "i"}

        books = list(books_collection.find(filters, {"_id": False}))

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
