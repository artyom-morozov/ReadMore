from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=300)
    description = models.TextField(default='')
    img_url = models.TextField()

class Rating(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    ratings = [
        (1, ''),
        (2, ''),
        (3, ''),
        (4, ''),
        (5, '')
    ]
    value = models.IntegerField(choices=ratings, default=1) 