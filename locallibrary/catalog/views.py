from django.shortcuts import render
from .models import Author, Book, BookInstance
from django.views import generic


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count() # метод all() применяется по умолчанию
    return render(request, template_name='index.html',
                  context={'num_books': num_books, 'num_instances': num_instances,
                           'num_instances_available': num_instances_available,
                           'num_authors': num_authors}
                           )


class BooksListView(generic.ListView):
    model = Book
    paginate_by=2 # активация встроенного пагинатора
    context_object_name = 'book_list' # Это значение по умолчанию
    # queryset = Book.objects.filter(title__icontains='war')[:5] # Кастомный запрос
    template_name = 'catalog/templates/book_list.html' # Дефолтный путь до шаблона

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