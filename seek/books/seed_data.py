# bo>>> >>> ations/seed_data.py
from books.models import books_collection

initial_data = [
    {"title": "Book One", "author": "Author A", "published_date": "2021-06-01", "genre": "Fiction", "price": 15.99},
    {"title": "Book Two", "author": "Author B", "published_date": "2020-07-15", "genre": "Non-Fiction", "price": 20.00},
    {"title": "Book Three", "author": "Author C", "published_date": "2021-05-10", "genre": "Science Fiction", "price": 18.50},
    {"title": "Book Four", "author": "Author D", "published_date": "2022-01-20", "genre": "Fantasy", "price": 25.00},
    {"title": "Book Five", "author": "Author E", "published_date": "2023-03-05", "genre": "Mystery", "price": 12.75},
]

books_collection.insert_many(initial_data)
