from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.index, name='index'),
    path('books/', view=views.BooksListView.as_view(), name='books'),
    path(r'^book/(?P<pk>\d+)$', view=views.BookDetailView.as_view(), name='book_detail'),
    path('authors/', view=views.AuthorsListView.as_view(), name='authors'),
    path(r'^author/(?P<pk>\d+)$', view=views.AuthorDetailView.as_view(), name='author_detail'),
    path(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]