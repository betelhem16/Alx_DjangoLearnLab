from django.contrib import admin

# Register your models here.

from .models import Book

# Customizing the Admin Interface for Book model
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Show these fields in the list view
    search_fields = ('title', 'author')  # Enable search by title and author
    list_filter = ('publication_year',)  # Add filter for publication year

# Register the Book model with the custom admin settings
admin.site.register(Book, BookAdmin)
