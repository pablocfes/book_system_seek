# books/urls.py
from django.urls import path
from books.api.views import BookView, AveragePriceView

urlpatterns = [
    path('books/', BookView.as_view(), name='book-list-create'),
    path('books/average-price/<int:year>/', AveragePriceView.as_view(), name='average-price'),
]
