from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from books.models import books_collection
from books.api.serializers import BookSerializer
from bson.objectid import ObjectId

class BookView(APIView):

    def get(self, request):
        # Filtrar por query_params
        filters = {}
        for param in ['title', 'author', 'published_date', 'price']:
            value = request.query_params.get(param)
            if value:
                filters[param] = {"$regex": value, "$options": "i"}

        # Buscar libros según los filtros
        books = list(books_collection.find(filters, {"_id": 0}))
        if not books:
            return Response({"message": "No books found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(books, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            books_collection.insert_one(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
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

    def delete(self, request):
        title = request.data.get('title')
        if not title:
            return Response({"error": "Title is required for deleting a book"}, status=status.HTTP_400_BAD_REQUEST)

        result = books_collection.delete_one({"title": title})
        if result.deleted_count == 0:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Book deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


    

class AveragePriceView(APIView):
    def get(self, request, year):
        pipeline = [
            {"$match": {"published_date": {"$regex": f"^{year}"}}},
            {"$group": {"_id": None, "average_price": {"$avg": "$price"}}}
        ]
        result = list(books_collection.aggregate(pipeline))
        if result:
            return Response({"average_price": result[0]["average_price"]})
        return Response({"average_price": 0})
