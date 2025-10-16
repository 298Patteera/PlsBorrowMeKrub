from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group
from authen.forms import RegistForm


class LoginView(View):
    
    def get(self, request):
        # code here
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    
    def post(self, request):
        # code here
        form = AuthenticationForm(data=request.POST)
        print("Yess")
        if form.is_valid():
            print("yess form is valid")
            user = form.get_user()
            login(request, user)
            print("user: ", user)
            return redirect("home-page")
        print("error", form.errors)
        return render(request, "login.html", {"form": form})
    
class RegisterView(View):
    def get(self, request):
        form = RegistForm()
        return render(request, 'register.html', {"form": form})

    def post(self, request):
        form = RegistForm(request.POST)

        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='user')
            user.groups.add(group)
            login(request, user)
            return redirect("login")
        print(form.errors)
        return render(request, "register.html", {"form": form})

class LogoutView(View):
    
    def get(self, request):
        # code here
        logout(request)
        return redirect("login")