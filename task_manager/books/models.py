from django.db import models
from administration.models import Author
# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    pages = models.IntegerField()
    amount = models.IntegerField()
    language = models.CharField(max_length=30)
    published_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ManyToManyField(Author)

    def __str__(self):
        return self.title