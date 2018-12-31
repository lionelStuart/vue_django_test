from django.contrib import admin
from django.urls import path, include

from myapp import views

urlpatterns = [
    path('show_book', views.show_book),
]
