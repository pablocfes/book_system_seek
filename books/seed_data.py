# bo>>> >>> ations/seed_data.py
from books.models import books_collection

initial_data = [
    {"title": "Cien años de soledad", "author": "Gabriel García Márquez", "published_date": "1967-05-30", "genre": "Novela", "price": 15.99},
    {"title": "1984", "author": "George Orwell", "published_date": "1949-06-08", "genre": "Novela", "price": 12.99},
    {"title": "El nombre de la rosa", "author": "Umberto Eco", "published_date": "1984-07-15", "genre": "Novela", "price": 9.99},
    {"title": "El senor de los anillos", "author": "JRR Tolkien", "published_date": "1954-07-29", "genre": "Novela", "price": 19.99},
    {"title": "El diario de Ana Frank", "author": "Ana Frank", "published_date": "1947-08-15", "genre": "Novela", "price": 11.99},
    {"title": "Inside Out", "author": "Pete Docter", "published_date": "2019-06-06", "genre": "Animación", "price": 14.99},
    {"title": "Toy Story", "author": "John Lasseter", "published_date": "1995-11-22", "genre": "Animación", "price": 12.99},
    {"title": "The Lion King", "author": "Roger Allers", "published_date": "1994-07-29", "genre": "Animación", "price": 10.99},
    {"title": "Frozen", "author": "Chris Buck", "published_date": "2013-11-27", "genre": "Animación", "price": 14.99},
    {"title": "Moana", "author": "Ron Clements", "published_date": "2016-11-23", "genre": "Animación", "price": 12.99},
    {"title": "The Hobbit", "author": "JRR Tolkien", "published_date": "1937-09-21", "genre": "Novela", "price": 14.99},
    {"title": "El ultimo beso", "author": "Javier Bonnet", "published_date": "2013-07-15", "genre": "Novela", "price": 19.99},
    {"title": "Adin", "author": "Umberto Eco", "published_date": "2019-07-15", "genre": "Novela", "price": 25.99},
]

def insert_initial_data():
    for book in initial_data:
        existing_book = books_collection.find_one({"title": book["title"]})
        if not existing_book:
            print(f"Se inserta el libro {book['title']}")
            books_collection.insert_one(book)
        else:
            print(f"El libro {book['title']} ya existe en la base de datos")

if __name__ == "__main__":
    insert_initial_data()