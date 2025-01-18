from datetime import date
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a book genre\
                            (e.g.: Scince Fiction, French Poetry, Novel etc.")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(max_length=1000,
                               help_text='Enter a short decription of the book')
    isbn = models.CharField(verbose_name='ISBN', max_length=13,
                            help_text='13 character: <a href=\
                                "https://www.isbn-international.org/content/what-isbn">\
                                    ISBN Number</a>')
    genre = models.ManyToManyField(to=Genre, help_text='Select a genre for this boook')
    # Если модель, в ForeignKey еще не определена, то указывается в виде строки
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def display_list_of_genres(self):
        return ', '.join([i.name for i in self.genre.all()[:3]])

    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.id)])


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Generate unique ID for this partcular\
                            book across whole library')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200, help_text="version info")
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    LOAN_STATUS = (
        ('m', 'Maintance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True,
                              default='m', help_text='Book availability')

    class Meta:
        ordering = ['due_back']
        permissions = (('can_view_all_book_instance_on_loan', 'view'),)

    def __str__(self):
        return '{} {}'.format(self.id, self.book.title)

    def is_overdue(self):
        return self.due_back and self.due_back < date.today()


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('author_detail', args=[str(self.id)])

    def __str__(self):
        return '{} {}'.format(self.first_name, self.second_name)


