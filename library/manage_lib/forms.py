from django.forms import ModelForm, SplitDateTimeField
from django.forms.widgets import Textarea, TextInput, SplitDateTimeWidget, TimeInput, FileInput, HiddenInput
from django.core.exceptions import ValidationError

from django import forms
from manage_lib.models import Book ,Author, Category

class LibAddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
    
    def clean(self):
        cleaned_data = super().clean()
        book_id = cleaned_data.get("book_id")
        category = cleaned_data.get("category")

        if category and book_id:
            if category.name == "Novel" and not book_id.startswith("01"):
                raise ValidationError("Book ID สำหรับ Novel ต้องเริ่มต้นด้วย '01'")
            elif category.name == "Fantasy" and not book_id.startswith("02"):
                raise ValidationError("Book ID สำหรับ Fantasy ต้องเริ่มต้นด้วย '02'")
            elif category.name == "Sci-Fi" and not book_id.startswith("03"): 
                raise ValidationError("Book ID สำหรับ Sci-Fi ต้องเริ่มต้นด้วย '03'")
            elif category.name == "Thriller" and not book_id.startswith("04"):
                raise ValidationError("Book ID สำหรับ Thriller ต้องเริ่มต้นด้วย '04'")
            elif category.name == "Phycology" and not book_id.startswith("05"):
                raise ValidationError("Book ID สำหรับ Phycology ต้องเริ่มต้นด้วย '05'")
            
        return cleaned_data

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

class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']

class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
