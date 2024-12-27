from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from .models import Author, Book, BookInstance
from django.views import generic


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # метод all() применяется по умолчанию

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(request, template_name='index.html',
                  context={'num_books': num_books, 'num_instances': num_instances,
                           'num_instances_available': num_instances_available,
                           'num_authors': num_authors, 'num_visits': num_visits}
                  )


class BooksListView(generic.ListView):
    model = Book
    paginate_by = 2  # активация встроенного пагинатора
    context_object_name = 'book_list'  # Это значение по умолчанию
    # queryset = Book.objects.filter(title__icontains='war')[:5] # Кастомный запрос
    template_name = 'catalog/templates/book_list.html'  # Дефолтный путь до шаблона

    # добавление данных в контекст переопределением внутреннего метода
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['some_custom_data'] = 'custom_data'
        return context


class BookDetailView(generic.DetailView):
    model = Book


class AuthorsListView(generic.ListView):
    model = Author
    paginate_by = 2
    context_object_name = 'author_list'
    template_name = 'catalog/templates/author_list.html'


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')