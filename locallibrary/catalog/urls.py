from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.index, name='index'),
    path('books/', view=views.BooksListView.as_view(), name='books'),
    path('book/<int:pk>', view=views.BookDetailView.as_view(), name='book_detail'),
    path('authors/', view=views.AuthorsListView.as_view(), name='authors'),
    path('author/<int:pk>', view=views.AuthorDetailView.as_view(), name='author_detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('librarian/', views.AllLoanedBooksForStaff.as_view(), name='librarian-page'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path("author/create/", views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
    path('book/create/', views.BookCreate.as_view(), name='book_create'),
]