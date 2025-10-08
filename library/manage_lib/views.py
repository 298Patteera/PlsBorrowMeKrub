from django.shortcuts import render, redirect

from manage_lib.models import *

from django.views import View

from .forms import *

# Create your views here.

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
    

class AddBookViews(View):
    def get(self, request):
        add_book_form = LibAddBookForm()

        return render(request, "libra_add_book.html", context={
            "add_book_form": add_book_form
        })
    
    def post(self, request):
        add_book_form = LibAddBookForm(request.POST, request.FILES)
        if add_book_form.is_valid():
            add_book_form.save()
            return redirect("home-page")
        return render(request, "libra_add_book.html", {
            "add_book_form": add_book_form
        })

class BookDetailsViews(View):
    def get(self, request, book_id):
        book_list = Book.objects.get(pk=book_id)

        return render(request, "book_details.html", context={
            "book_list":book_list
        })
    
class UpdateBookViews(View):
    def get(self, request, book_id):
        book_update = Book.objects.get(pk=book_id)

        book_update_form = LibUpdateBookForm(instance=book_update)

        return render(request, "libra_update_book.html", context= {
            "book_update": book_update,
            "book_update_form": book_update_form,
        })
    