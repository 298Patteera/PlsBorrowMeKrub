from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegistForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-blue-300 rounded-lg '
                     'focus:outline-none focus:ring-2 focus:ring-blue-400 '
                     'focus:border-transparent transition'
        }),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            "username": forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-blue-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition'
            }),
            "first_name": forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-blue-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition'
            }),
            "last_name": forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-blue-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition'
            }),
            "email": forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-blue-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition'
            }),
            "password": forms.PasswordInput(attrs={
                'class': 'w-full px-4 py-2 border border-blue-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition'
            }),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Passwords do not match")
        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        # hash pwd
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
