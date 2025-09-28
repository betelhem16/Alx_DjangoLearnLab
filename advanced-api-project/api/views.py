
# Create your views here.
from rest_framework import generics , permissions
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


# List & Create Books
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# List & Create Authors
class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
# List all books (Read-only, accessible by anyone)
class BookListView(generics.ListAPIView):
    """
    GET /api/books/
    Returns a list of all books.
    Accessible by any user (authenticated or not).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# Retrieve a single book by ID (Read-only, accessible by anyone)
class BookDetailView(generics.RetrieveAPIView):
    """
    GET /api/books/<id>/
    Returns details of a single book.
    Accessible by any user.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# Create a new book (Only authenticated users)
class BookCreateView(generics.CreateAPIView):
    """
    POST /api/books/create/
    Creates a new book instance.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# Update an existing book (Only authenticated users)
class BookUpdateView(generics.UpdateAPIView):
    """
    PUT /api/books/update/<id>/
    Updates an existing book instance.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# Delete a book (Only authenticated users)
class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/books/delete/<id>/
    Deletes a book instance.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]