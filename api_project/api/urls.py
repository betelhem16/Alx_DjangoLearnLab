# api/urls.py
from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet


# Create router and register the ViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    
    # New CRUD endpoints (handled by router)
    path('', include(router.urls)),
]
