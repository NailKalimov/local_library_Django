from django.contrib import admin

from .models import Genre, Book, BookInstance, Author

# Register your models here.
admin.site.register(Genre)
# admin.site.register(Book)
# admin.site.register(BookInstance)

class BookInLine(admin.TabularInline):
    model = Book
"""по умолчанию модели в админке отображаются через ф-ю __str__,
но это можно кастомизировать с помощью класса %modelname%Admin(admin.ModelAdmin)"""
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'second_name', 'date_of_birth', 'date_of_death')
    list_filter = ('first_name', 'second_name',)
    ''' можем настроить отображаемые поля в форме создания
    если поля объединены в кортеж, они будут отображаться на одной строке'''
    fields = ['first_name', 'second_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInLine]
admin.site.register(Author, AuthorAdmin)


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_list_of_genree')
    list_filter = ('author', 'title',)
    inlines = [BooksInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'id')
    list_filter = ('status', 'due_back',)
    # Группировка полей в форме создания обьекта
    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )