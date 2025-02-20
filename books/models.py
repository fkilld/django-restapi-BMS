# books/models.py
from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    cat_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.cat_name

class Book(models.Model):
    book_name = models.CharField(max_length=100)
    book_description = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.book_name
