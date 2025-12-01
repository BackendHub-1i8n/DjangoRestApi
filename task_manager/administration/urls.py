from django.urls import path

from . import views

app_name = 'administration'

urlpatterns = [
    path('', views.index_admin, name='admin_index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('create_user', views.create_user, name='create_user'),
    path('user_details/<int:id>', views.user_details, name='user_details'),
    path('delete/user/<int:id>', views.delete_user, name='delete_user'),
    path('edit/user/<int:id>', views.edit_user, name='edit_user'),
    path('/user_reports', views.user_reports, name='user_reports'),
    path('authors', views.authors_list, name='authors_list'),
    path('authors/add', views.add_author, name='add_author'),
    path('authors/details/<int:id>', views.author_details, name='author_details'),
    path('authors/delete/<int:id>', views.delete_author, name='delete_author'),
    path('authors/statistics', views.author_statistics, name='author_statistics'),
    path('authors/edit/<int:id>', views.edit_author, name='edit_author'),
    path('/books', views.books_list, name='books_list'),
    path('/books/add', views.add_book, name='add_book'),
    path('/books/edit/<int:id>', views.edit_book, name='edit_book'),
    path('/books/delete/<int:id>', views.delete_book, name='delete_book'),
    path('logout', views.logout_user, name='auth_logout'),
]