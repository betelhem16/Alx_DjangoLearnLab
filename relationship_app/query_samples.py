import os
import sys
import django

# Add the parent directory to sys.path so Python can find LibraryProject
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(file))))

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# -----------------------------
# Query 1: All books by a specific author
# -----------------------------
author_name = "George Orwell"
try:
    author = Author.objects.get(name=author_name)
    books = Book.objects.filter(author=author)
    print(f"\nBooks by {author_name}: {[book.title for book in books]}")
except Author.DoesNotExist:
    print(f"\nAuthor '{author_name}' not found.")

# -----------------------------
# Query 2: List all books in a library
# -----------------------------
library_name = "Central Library"
try:
    library = Library.objects.get(name=library_name)
    books = library.books.all()
    print(f"\nBooks in {library_name}: {[book.title for book in books]}")
except Library.DoesNotExist:
    print(f"\nLibrary '{library_name}' not found.")

# -----------------------------
# Query 3: Retrieve the librarian for a library
# -----------------------------
try:
    librarian = Librarian.objects.get(library__name=library_name)
    print(f"\nLibrarian of {library_name}: {librarian.name}")
except Librarian.DoesNotExist:
    print(f"\nNo librarian assigned to {library_name}.")
