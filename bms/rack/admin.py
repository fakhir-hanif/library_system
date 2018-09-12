from django.contrib import admin
from .models import Book, Rack_books, Rack, Author


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'published', 'created_by', 'updated_by', 'updated_at')
    pass


class RackBooksAdmin(admin.ModelAdmin):
    list_display = ('book', 'rack')
    pass

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('f_name', 'l_name')


class RackAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_size', 'uid')

admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Rack, RackAdmin)
admin.site.register(Rack_books, RackBooksAdmin)
