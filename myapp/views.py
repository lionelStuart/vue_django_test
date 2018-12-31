import json

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from .models import Book


def show_book(request):
    response = {}
    try:
        books = Book.objects.all()
        response['first'] = json.loads(serializers.serialize('json', books))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)
