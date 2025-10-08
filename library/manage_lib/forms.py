from django.forms import ModelForm, SplitDateTimeField
from django.forms.widgets import Textarea, TextInput, SplitDateTimeWidget, TimeInput, FileInput, HiddenInput
from django.core.exceptions import ValidationError

from django import forms
from manage_lib.models import Book

class LibAddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        # ถ้าอยากใส่ widget กำหนดตรงนี้ได้ เช่น
        # widgets = {
        #     "details": forms.Textarea(attrs={"rows": 3}),
        #     "book_id": forms.TextInput(attrs={"placeholder": "Enter Book ID"}),
        # }
        widgets = {
            # "image": forms.HiddenInput()
            # 'image': FileInput(attrs={'class': 'hidden'})
            "book_img": FileInput(attrs={'class': 'hidden'}),
        }

class LibUpdateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        widgets = {
            # "image": forms.HiddenInput()
            # 'image': FileInput(attrs={'class': 'hidden'})
            "book_img": FileInput(attrs={'class': 'hidden'}),
            'book_id': forms.TextInput(attrs={'readonly': 'readonly'}),
        }