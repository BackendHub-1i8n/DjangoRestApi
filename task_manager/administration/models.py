from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    roles = [
        ('author', 'Author'),
        ('reader', 'Reader'),
        ('librarian', 'Librarian'),
    ]
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128, default='')
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=20, choices=roles, default='reader')

    REQUIRED_FIELDS = ['email', 'password']




    def __str__(self):
        return self.username


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    ci = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='person')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Author(models.Model):
    nacionality = models.CharField(max_length=50)
    biography = models.TextField()
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name='author_profile')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Reader(models.Model):
    membership_date = models.DateField()
    ru = models.CharField(max_length=10, unique=True)
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name='reader_profile')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Librarian(models.Model):
    hire_date = models.DateField()
    item = models.CharField(max_length=50)
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name='librarian_profile')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


