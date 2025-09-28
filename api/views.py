
# Create your views here.
from rest_framework import generics , permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


# List all books with filtering, searching, and ordering
"""
BookListView:
    - Supports filtering by: title, author, publication_year
    - Supports searching in: title, author name
    - Supports ordering by: title, publication_year
    Usage examples:
        /api/books/?title=The River Between
        /api/books/?search=River
        /api/books/?ordering=-publication_year
"""

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Enable filtering, searching, ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtering by these fields
    filterset_fields = ['title', 'author', 'publication_year']

    # Searching by title and author
    search_fields = ['title', 'author__name']  # assuming author has a "name" field

    # Ordering by title and publication year
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering

# List & Create Authors
class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
# List all books (Read-only, accessible by anyone)
#(2. Implementing Filtering, Searching, and Ordering in Django REST Framework)
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # public read access

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


