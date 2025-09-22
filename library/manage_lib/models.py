from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=20, unique=True, primary_key=True)
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    age = models.IntegerField(null=False)
    email = models.EmailField(max_length=300)
    password = models.CharField(max_length=120, null=False)
    is_librarian = models.BooleanField(default=False)

class Book(models.Model):
    book_id = models.CharField(max_length=10, unique=True, primary_key=True)
    title = models.CharField(max_length=100, null=False)
    details = models.TextField()
    categories = models.ManyToManyField('Category', blank=True)
    is_available = models.BooleanField(default=False)

class Category(models.Model):
    name = models.CharField(max_length=100)
    # book_cat = models.ManyToManyField(Book, blank=True)

class Author(models.Model):
    name = models.CharField(max_length=100)
    book_auth = models.ManyToManyField(Book, blank=True)

class Borrows(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    
    class BookStatus(models.TextChoices):
        BORROWING = "BR", _("Borrowing")
        RETURNED = "RE", _("Returned")

    book_status = models.CharField(
        max_length=2,
        choices=BookStatus
    )
