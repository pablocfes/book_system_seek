# books/urls.py
from django.urls import path
from books.api.views import BookView, AveragePriceView

urlpatterns = [
    path('crud/', BookView.as_view(), name='book-crud'),
    path('average-price/', AveragePriceView.as_view(), name='average-price'),
]
