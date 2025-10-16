from django.urls import path

from authen.views import LoginView, LogoutView, RegisterView



urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('logout', LogoutView.as_view(), name="logout")
]