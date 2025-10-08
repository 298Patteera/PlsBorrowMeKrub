from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeViews.as_view(), name="home-page"),
    path("bookdetails/<str:book_id>", views.BookDetailsViews.as_view(), name="book-details"),
    # path("/login", views.LoginViews.as_view(), name="login-page"),
    path("libaddbook", views.AddBookViews.as_view(), name="lib-add-book"),
    path("libupdatebook/<str:book_id>", views.UpdateBookViews.as_view(), name="lib-update-book"),
    # path("/libshowbook", views.ShowBookViews.as_view(), name="lib-show-book"),
    # path("/userbookshelf", views.UserBookShelfViews.as_view(), name="user-bookshelf"),
    # path("/userprofile", views.UserProfViews.as_view(), name="user-profile"),
    # path("/userregister", views.RegisterViews.as_view(), name="user-register"),
]