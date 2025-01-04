from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from users.models import User
from rest_framework.authtoken.models import Token

class BookViewTestCase(APITestCase):
    def setUp(self):
        # Configuración inicial para los tests, como datos de prueba o autenticación
        self.url = '/api/books/crud/'
        self.mock_book = {
            "_id": "mock_id",
            "title": "Test Book",
            "author": "Test Author",
            "published_date": "2022-01-01",
            "genre": "Fiction",
            "price": 20.0
        }

        self.usuario = User.objects.create_user(
            username='testuser',
            password='testpassword',
            first_name='John',
            last_name='Doe',
            email='0aOY5@example.com'
        )

        self.token = Token.objects.create(user=self.usuario)

        # Simular autenticación del usuario con token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    @patch('books.models.books_collection.find')
    def test_get_books_success(self, mock_find):
        # Simula el retorno de documentos en MongoDB
        mock_find.return_value = [self.mock_book]
        response = self.client.get(self.url, {'title': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('books', response.data)

    @patch('books.models.books_collection.find')
    def test_get_books_not_found(self, mock_find):
        # Simula que no se encuentran libros
        mock_find.return_value = []
        response = self.client.get(self.url, {'title': 'Nonexistent'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'No books found')

    @patch('books.models.books_collection.insert_one')
    @patch('books.models.books_collection.find_one')
    def test_post_book_success(self, mock_find_one, mock_insert_one):
        # Simula que el libro no existe y luego se inserta
        mock_find_one.return_value = None
        mock_insert_one.return_value.inserted_id = "mock_id"
        response = self.client.post(self.url, self.mock_book, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.mock_book['title'])

    @patch('books.models.books_collection.find_one')
    def test_post_book_already_exists(self, mock_find_one):
        # Simula que el libro ya existe
        mock_find_one.return_value = self.mock_book
        response = self.client.post(self.url, self.mock_book, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.mock_book['title'])

    @patch('books.models.books_collection.update_one')
    def test_patch_book_success(self, mock_update_one):
        # Simula una actualización exitosa
        mock_update_one.return_value.matched_count = 1
        response = self.client.patch(self.url, {'title': 'Test Book', 'price': 25.0}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Book updated successfully')

    @patch('books.models.books_collection.update_one')
    def test_patch_book_not_found(self, mock_update_one):
        # Simula que no se encontró el libro para actualizar
        mock_update_one.return_value.matched_count = 0
        response = self.client.patch(self.url, {'title': 'Nonexistent Book'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Book not found')

    @patch('books.models.books_collection.delete_one')
    def test_delete_book_success(self, mock_delete_one):
        # Simula una eliminación exitosa
        mock_delete_one.return_value.deleted_count = 1
        response = self.client.delete(self.url, {'title': 'Test Book'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch('books.models.books_collection.delete_one')
    def test_delete_book_not_found(self, mock_delete_one):
        # Simula que no se encontró el libro para eliminar
        mock_delete_one.return_value.deleted_count = 0
        response = self.client.delete(self.url, {'title': 'Nonexistent Book'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Book not found')