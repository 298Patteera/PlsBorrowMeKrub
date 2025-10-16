from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.

# class User(models.Model):
#     username = models.CharField(max_length=20, unique=True, primary_key=True)
#     first_name = models.CharField(max_length=150, null=False)
#     last_name = models.CharField(max_length=150, null=False)
#     age = models.IntegerField(null=False)
#     email = models.EmailField(max_length=300)
#     password = models.CharField(max_length=120, null=False)
#     is_librarian = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.username}"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"

class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"
    
class Book(models.Model):
    book_id = models.CharField(max_length=10, unique=True, primary_key=True)
    title = models.CharField(max_length=100, null=False)
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    authors = models.ManyToManyField('Author', blank=True)
    avai_amount = models.IntegerField(null=False)
    book_img = models.FileField(upload_to="image/", blank=True, null=True)

    def __str__(self):
        return f"{self.book_id}"



class Borrows(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    

