from django.shortcuts import render
from django.http import HttpResponse

books = [
    {
        'author': 'Jack London',
        'title': 'Martin Eden',
        'ISBN': '1313123'
    },
    {
        'author': 'Remarque',
        'title': 'All Quite',
        'ISBN': '32313'
    }
]


def home(request):
    context = {
        'books': books
    }
    return render(request, 'read/home.html', context)
# Create your views here.

def about(request):
    return render(request, 'read/about.html')