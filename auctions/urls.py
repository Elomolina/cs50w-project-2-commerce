from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("listings/<int:id>", views.listing_detail, name = "listing_detail"),
    path("listings/user/<int:id>", views.userListings, name = "userListings"),
    path("watchlist", views.watch, name = "watch"),
    path("watchlist/<int:id>", views.watchlist, name = "watchlist"),
    path("categories/", views.categories, name = "categories"),
    path("categories/<int:id>", views.category_detail, name = "category_detail"), 
    path("myListings", views.myListings, name = "myListings"),
]
