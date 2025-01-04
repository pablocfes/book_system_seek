# urls.py
from django.urls import path
from users.api import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),

]