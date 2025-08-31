from bookshelf.models import Book

# Delete the book you created
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
# Expected Output: (1, {'bookshelf.Book': 1})

# Confirm deletion by retrieving all books
Book.objects.all()
# Expected Output: <QuerySet []>


