from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)      # Required by ALX
    author = models.CharField(max_length=100)     # Required by ALX
    publication_year = models.IntegerField()      # Required by ALX

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"


