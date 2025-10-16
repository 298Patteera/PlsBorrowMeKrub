from django.shortcuts import render, redirect

from manage_lib.models import *

from django.views import View

from .forms import *

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from django.db.models import F, Q
from django.contrib import messages

# Create your views here.

def is_libra(user, librarian):
    if user == librarian:
        return True
    return False

class HomeViews(View):
    
    def get(self, request):
        novel_list = Book.objects.filter(pk__startswith="01")
        fantasy_list = Book.objects.filter(pk__startswith="02")
        scifi_list = Book.objects.filter(pk__startswith="03")
        thriller_list = Book.objects.filter(pk__startswith="04")
        phycology_list = Book.objects.filter(pk__startswith="05")


        return render(request, 'index.html', context={
            "novel_list": novel_list,
            "fantasy_list": fantasy_list,
            "scifi_list": scifi_list,
            "thriller_list": thriller_list,
            "phycology_list": phycology_list,
        })
    

class AddBookViews(PermissionRequiredMixin, views.View):
    permission_required = 'manage_lib.add_book'
    
    def get(self, request):
        add_book_form = LibAddBookForm()

        return render(request, "libra_add_book.html", context={
            "add_book_form": add_book_form
        })
    
    def post(self, request):
        add_book_form = LibAddBookForm(request.POST, request.FILES)
        if add_book_form.is_valid():
            add_book_form.save()
            return redirect("lib-show-book")
        return render(request, "libra_add_book.html", {
            "add_book_form": add_book_form
        })

class BookDetailsViews(PermissionRequiredMixin, views.View):
    permission_required = 'manage_lib.view_book'

    def get(self, request, book_id):
        book_list = get_object_or_404(Book, book_id=book_id)
        borrow_book = Borrows.objects.filter(book=book_list)

        return render(request, "book_details.html", context={
            "book_list": book_list,
            "borrow_count": borrow_book.count()
        })
    
class UpdateBookViews(PermissionRequiredMixin, views.View):
    permission_required = 'manage_lib.change_book'

    def get(self, request, book_id):
        book_update = get_object_or_404(Book, pk=book_id)
        book_update_form = LibUpdateBookForm(instance=book_update)

        return render(request, "libra_update_book.html", context={
            "book_update": book_update,
            "book_update_form": book_update_form,
        })
    
    def post(self, request, book_id):
        book_update = get_object_or_404(Book, pk=book_id)
        book_update_form = LibUpdateBookForm(request.POST, request.FILES, instance=book_update)
        if book_update_form.is_valid():
            book_update_form.save()
            return redirect("lib-show-book")
        return render(request, "libra_update_book.html", context={
            "book_update": book_update,
            "book_update_form": book_update_form,
        })


class UserBookShelfViews(PermissionRequiredMixin, views.View):
    permission_required = 'manage_lib.view_borrows'

    def get(self, request):
        borrow_list = Borrows.objects.filter(user=request.user)

        return render(request, "user_bookshelf.html", context= {
            "borrow_list": borrow_list,
        })       

class UserProfViews(PermissionRequiredMixin, views.View):
    permission_required = 'auth.view_user'

    def get(self, request):
        return render(request, "user_profile.html", context={
            "user": request.user
        })
    
class AddAuthorView(PermissionRequiredMixin, View):
    permission_required = 'manage_lib.add_author'

    def get(self, request):
        form = AddAuthorForm()
        return render(request, 'libra_add_author.html', {'form': form})

    def post(self, request):
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lib-show-book')
        return render(request, 'libra_add_author.html', {'form': form})


class AddCategoryView(PermissionRequiredMixin, View):
    permission_required = 'manage_lib.add_category'

    def get(self, request):
        form = AddCategoryForm()
        return render(request, 'libra_add_category.html', {'form': form})

    def post(self, request):
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lib-show-book')
        return render(request, 'libra_add_category.html', {'form': form})
    
class UserBorrowBook(PermissionRequiredMixin, View):
    permission_required = 'manage_lib.add_borrows'

    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)

        if book.avai_amount <= 0:
            messages.error(request, "หนังสือเล่มนี้ถึงขีดจำกัดการยืมแล้ว")
            return redirect('book-details', book_id=book_id)

        existing_borrow = Borrows.objects.filter(user=request.user, book=book, return_date__isnull=True).first()
        if existing_borrow:
            messages.error(request, "หนังสือเล่มนี้อยู่ในชั้นหนังสือของคุณแล้ว")
            return redirect('book-details', book_id=book_id)

        with transaction.atomic():
            borrow_date = timezone.now().date()
            due_date = borrow_date + timedelta(days=7)
            Borrows.objects.create(user=request.user, book=book, due_date=due_date)
            
            book.avai_amount = F('avai_amount') - 1
            book.save()

        return redirect('user-bookshelf')
    
class UserReturnBook(PermissionRequiredMixin, View):
    permission_required = 'manage_lib.change_borrows'

    def post(self, request, borrow_id):
        borrow = get_object_or_404(Borrows, pk=borrow_id, user=request.user)
        
        
        with transaction.atomic():
            borrow.return_date = timezone.now().date()
            borrow.save()
            
            borrow.book.avai_amount = F('avai_amount') + 1
            borrow.book.save()
        
        return redirect('user-bookshelf')

class BookSearchViews(View):
    def get(self, request):
        book_list = Book.objects.all()

        search = request.GET.get("q", "")
        option = request.GET.get("filter", "title")

        if search:
            if option == "author":
                #M2M
                book_list = book_list.filter(authors__name__icontains=search).distinct()
            else:
                book_list = book_list.filter(title__icontains=search)

        return render(request, "book_search.html", context = {
            "book_list": book_list,
            "search": search,
            "filter": option,
            "total": book_list.count()
        })

class ShowBookViews(PermissionRequiredMixin, views.View):
    permission_required = 'manage_lib.add_book'

    def get(self, request):
        book_list = Book.objects.all()
        author_list = Author.objects.all()

        return render(request, "libra_show_all_book.html", context={
            "book_list": book_list,
            "author_list": author_list
        })

class DeleteBookViews(PermissionRequiredMixin, views.View):
    permission_required = 'manage_lib.delete_book'

    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        book.delete()
        print("eiei")
        return redirect("lib-show-book")