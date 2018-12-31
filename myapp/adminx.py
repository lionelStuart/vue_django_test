import xadmin

from .models import Book


class BookAdminx(object):
    list_display = ('book_name', 'add_time')


xadmin.site.register(Book, BookAdminx)
