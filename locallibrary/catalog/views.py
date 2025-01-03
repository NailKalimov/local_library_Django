import datetime
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import RenewBookForm
from .models import Author, Book, BookInstance
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author


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


class AllLoanedBooksForStaff(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_on_loan_for_staff.html'
    permission_required = 'catalog.can_view_all_book_instance_on_loan'


@permission_required('catalog.can_view_all_book_instance_on_loan')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            return HttpResponseRedirect(reverse('librarer-page'))

        return render(request, 'catalog/book_renew_librarian.html',
                      {'form': form, 'book_inst': book_inst})
    else:
        default_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': default_renewal_date})
        return render(request, 'catalog/book_renew_librarian.html',
                      {'form': form, 'bookinst': book_inst})


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '12/10/2016', }


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
