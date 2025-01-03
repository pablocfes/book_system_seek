from rest_framework import serializers

class BookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    author = serializers.CharField(max_length=255)
    published_date = serializers.DateField()
    genre = serializers.CharField(max_length=100)
    price = serializers.FloatField()