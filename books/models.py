# Importing the models module from Django's ORM to define database models
from django.db import models 

# Importing Django's built-in User model for authentication and user management
from django.contrib.auth.models import User  

# Defining the Author model, which represents authors of books
class Author(models.Model):
    # ForeignKey relation with User model to link an author to a registered user
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    # CharField to store the author's name with a maximum length of 100 characters
    name = models.CharField(max_length=100)  
    
    # String representation of the model, which returns the author's name
    def __str__(self):  
        return self.name  

# Defining the Category model, which represents different categories a book can belong to
class Category(models.Model):
    # CharField to store the category name with a maximum length of 100 characters
    cat_name = models.CharField(max_length=100)  
    
    # String representation of the model, which returns the category name
    def __str__(self):  
        return self.cat_name  

# Defining the Book model, which represents books in the system
class Book(models.Model):
    # CharField to store the book's name with a maximum length of 100 characters
    book_name = models.CharField(max_length=100)  
    # TextField to store a detailed description of the book
    book_description = models.TextField()  
    # ForeignKey relation linking the book to a specific author (one-to-many relationship)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  
    # Many-to-Many relation allowing a book to be associated with multiple categories
    categories = models.ManyToManyField(Category)  
    # ForeignKey relation linking the book to the user who added it (one-to-many relationship)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    
    # String representation of the model, which returns the book's name
    def __str__(self):  
        return self.book_name  
