from django.contrib import admin

# Register your models here.
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_name', 'add_time')
