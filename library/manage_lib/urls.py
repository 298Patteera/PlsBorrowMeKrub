from django.urls import path

from . import views



urlpatterns = [
    path("", views.HomeViews.as_view(), name="home-page"),
    path("bookdetails/<str:book_id>/", views.BookDetailsViews.as_view(), name="book-details"),
    path("booksearch/", views.BookSearchViews.as_view(), name="book-search"),
    path("libaddbook/", views.AddBookViews.as_view(), name="lib-add-book"),
    path("libupdatebook/<str:book_id>/", views.UpdateBookViews.as_view(), name="lib-update-book"),
    path("libdeletebook/<str:book_id>/", views.DeleteBookViews.as_view(), name="lib-delete-book"),
    path("libshowbook/", views.ShowBookViews.as_view(), name="lib-show-book"),
    path("userbookshelf/", views.UserBookShelfViews.as_view(), name="user-bookshelf"),
    path("userprofile/", views.UserProfViews.as_view(), name="user-profile"),
    path("borrow/<str:book_id>/", views.UserBorrowBook.as_view(), name="borrow-book"),
    path("return/<int:borrow_id>/", views.UserReturnBook.as_view(), name="return-book"),
    path('libaddauthor/', views.AddAuthorView.as_view(), name='lib-add-author'),
    path('libaddcategory/', views.AddCategoryView.as_view(), name='lib-add-category'),

]