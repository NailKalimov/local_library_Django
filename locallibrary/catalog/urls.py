from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.index, name='index'),
    path('books/', view=views.BooksListView.as_view(), name='books'),
    path(r'^book/(?P<pk>\d+)$', view=views.BookDetailView.as_view(), name='book_detail'),
    path('authors/', view=views.AuthorsListView.as_view(), name='authors'),
    path(r'^author/(?P<pk>\d+)$', view=views.AuthorDetailView.as_view(), name='author_detail'),
    path(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('librarer/', views.AllLoanedBooksForStaff.as_view(), name='librarer-page'),
    path(r'^book/(?<pk>[-\w]+/renew/$)', views.renew_book_librarian, name='renew-book-librarian'),
    path(r'author/create/$', views.AuthorCreate.as_view(), name='author_create'),
    path(r'^author/(?P<pk>\d+)/update/$', views.AuthorUpdate.as_view(), name='author_update'),
    path(r'^author/(?P<pk>\d+)/delete/$', views.AuthorDelete.as_view(), name='author_delete'),
]