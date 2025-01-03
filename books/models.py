# books/models.py
from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]
books_collection = db['books']
