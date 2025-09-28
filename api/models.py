from django.db import models

# Create your models here.
# Author model to store book authors
class Author(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name
#book model linked to Author
class Book(models.Model):
    title=models.CharField(max_length=200)
    publication_year=models.IntegerField()
    #one author can have many books
    author=models.ForeignKey(Author, related_name='books' , on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.title} ({self.publication_year})"