from django.contrib import admin
from administration.models import Author,Person, Reader,Librarian,User
# Register your models here.
admin.site.register([
    Author,
    Person,
    Reader,
    Librarian,
    User
])