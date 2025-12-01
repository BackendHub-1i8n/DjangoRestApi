from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.templatetags.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from administration.models import User, Person, Author
from administration.forms.create_author_form import CreateAuthorForm
from administration.forms.edit_author_form import EditAuthorForm
from books.models import Book
from .decorators import admin_required, librarian_or_admin_required
from books.forms.create_book import BookForm

# Create your views here.
nav_links = [
        {
            'label': "Dashboard",
            'icon': 'fas fa-chart-line',
            'children': [
                {
                    'label': "Overview",
                    'to': "administration:dashboard",
                    'icon': 'fas fa-tachometer-alt',
                },
                {
                    'label': "Create User",
                    'to': "administration:create_user",
                    'icon': 'fas fa-user-plus',
                },
                {
                    'label': "Reports",
                    'to': "administration:user_reports",
                    'icon': 'fas fa-file-alt',
                },
            ]
        },
        {
            'label': "Authors",
            'icon': 'fas fa-user-edit',
            'children': [
                {
                    'label': "Authors List",
                    'to': "administration:authors_list",
                    'icon': 'fas fa-list',
                },
                {
                    'label': "Add Author",
                    'to': "administration:add_author",
                    'icon': 'fas fa-user-plus',
                }
            ]
        },
        {
            'label': "Books",
            'icon': 'fas fa-book',
            'children': [
                {
                    'label': "Books List",
                    'to': "administration:books_list",
                    'icon': 'fas fa-list',
                },
                {
                    'label': "Add Book",
                    'to': "administration:add_book",
                    'icon': 'fas fa-book-medical',
                }
            ]
        }
    ]

@login_required
def index_admin(request):


    context = {
        'admin_nav': nav_links,
        'current_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'page_title': "Admin Dashboard"
    }

    return render(request, 'admins_index.html', context)

# Dashboard
@login_required
def dashboard(request):
    users = User.objects.all()

    # print all users to console
    for user in users:
        print(user)

    return render(request, 'people/index.html', context={'admin_nav': nav_links, 'page_title': "Dashboard", "users": users})

@login_required
def create_user(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            return render(request, 'people/create_user.html', context={'admin_nav': nav_links, 'page_title': "Create User", "shinobu": static("img/Shinobu.jpg"), 'error_message': "Passwords do not match."})
        is_superuser = 'is_superuser' in request.POST
        is_active = 'is_active' in request.POST
        role = request.POST.get('role')
        if role:
            role = role.lower()
        else:
            role = 'reader'
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            is_superuser=is_superuser,
            is_active=is_active,
            role=role
        )
        user.save()

        person = Person.objects.create(
            first_name=first_name,
            last_name=last_name,
            ci=request.POST['ci'],
            phone=request.POST['phone'],
            address=request.POST['address'],
            birth_date=request.POST['birth_date'],
            user=user
        )
        person.save()

        return redirect('administration:dashboard')
    return render(request, 'people/create_user.html', context={'admin_nav': nav_links, 'page_title': "Create User", "shinobu": static("img/Shinobu.jpg")})


def user_details(request, id):
    user = User.objects.get(pk=id)
    person = Person.objects.get(user=user)
    return render(request, 'people/manage_user.html', context={'admin_nav': nav_links, 'page_title': "Manage User", "user": user, "person": person})

@login_required
def delete_user(request, id):
    user = User.objects.get(pk=id)
    user.delete()
    return redirect('administration:dashboard')

@login_required
def edit_user(request, id):
    user = User.objects.get(pk=id)
    person = Person.objects.get(user=user)
    if request.method == "POST":
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        is_superuser = 'is_superuser' in request.POST
        is_active = 'is_active' in request.POST
        user.is_superuser = is_superuser
        user.is_active = is_active
        user.save()
        person.ci = request.POST['ci']
        person.phone = request.POST['phone']
        person.address = request.POST['address']
        person.birth_date = request.POST['birth_date']
        person.save()
        return redirect('administration:manage_users', id=id)
    return render(request, 'people/edit_user.html', context={'admin_nav': nav_links, 'page_title': "Edit User", "user": user, "person": person, "shinobu": static("img/Shinobu.jpg")})

def  user_reports(request):
    return HttpResponse("User Reports Page")

# Authors
def authors_list(request):
    persons = Person.objects.all()
    authors = Author.objects.all()

    authors_list = []
    for author in authors:
        person = author.person
        authors_list.append({
            'id': author.id,
            'first_name': person.first_name,
            'last_name': person.last_name,
            'nacionality': author.nacionality,
            'biography': author.biography,
        })

    return render(request, 'authors/index.html', context={'admin_nav': nav_links, 'page_title': "Authors List", "authors": authors_list})



def add_author(request):
    context = {
        'admin_nav': nav_links,
        'page_title': "Add Author",
        "shinobu": static("img/ether.png")
    }

    if request.method == "POST":
        form = CreateAuthorForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Author profile created successfully!")
                return redirect('administration:authors_list')
            except Exception as e:
                print(f"Error saving Author: {e}")
                context['general_error'] = "An unexpected database error occurred. Please try again."
                context['form'] = form
                return render(request, 'authors/create.html', context)

        else:
            context['form'] = form
            return render(request, 'authors/create.html', context)

    else:
        # GET request
        form = CreateAuthorForm()

    context['form'] = form
    return render(request, 'authors/create.html', context)


def author_details(request, id):
    author = Author.objects.get(pk=id)
    person = author.person

    books = Book.objects.filter(author=author)

    return render(request, 'authors/details.html', context={
        'admin_nav': nav_links,
        'page_title': "Author Details",
        "author": author,
        "person": person,
        "books": books
    })

def delete_author(request):
    return HttpResponse("Author Reports Page")

def author_statistics(request):
    return HttpResponse("Author Statistics Page")


def edit_author(request, id):
    author = get_object_or_404(Author, pk=id)
    person = author.person

    context = {
        'admin_nav': nav_links,
        'page_title': "Edit Author",
        "shinobu": static("img/ether2.png"),
        "author": author,
        "person": person,
    }

    if request.method == "POST":
        form = EditAuthorForm(request.POST, instance=author)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, f"Author {person.first_name} {person.last_name} updated successfully!")

                return redirect('administration:author_details', id=author.id)

            except Exception as e:
                messages.error(request, "An unexpected error occurred while saving the changes.")

    else:
        form = EditAuthorForm(instance=author)

    context['form'] = form
    return render(request, 'authors/edit.html', context)


# Books
def books_list(request):
    """Muestra la lista de todos los libros."""
    books = Book.objects.all().prefetch_related('author').order_by('-created_at')

    context = {
        'admin_nav': nav_links,  # Asumiendo que nav_links está disponible
        'page_title': "Book Management",
        'books': books,
    }
    return render(request, 'books/index.html', context)


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Book '{form.cleaned_data['title']}' registered successfully.")
            return redirect('administration:books_list')
    else:
        form = BookForm()

    context = {
        'admin_nav': nav_links,
        'page_title': "Register New Book",
        'form': form,
        'is_edit': False,
        'shinobu': static("img/ether.png"),
    }
    return render(request, 'books/form.html', context)


def edit_book(request, id):
    book = get_object_or_404(Book, pk=id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f"Book '{book.title}' updated successfully.")
            return redirect('administration:books_list')
    else:
        form = BookForm(instance=book)

    context = {
        'admin_nav': nav_links,
        'page_title': f"Edit Book: {book.title}",
        'form': form,
        'book': book,
        'is_edit': True,
        'shinobu': static("img/ether.png"),
    }
    return render(request, 'books/form.html', context)


def delete_book(request, id):
    book = get_object_or_404(Book, pk=id)

    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f"Book '{book_title}' deleted successfully.")
        return redirect('administration:books_list')

    context = {
        'admin_nav': nav_links,
        'page_title': f"Confirm Deletion: {book.title}",
        'book': book,
    }
    return render(request, 'books/confirm_delete.html', context)

@login_required
def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('auth_login')