from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new-listing"),
    path("show_listing/<int:pk>", views.show_listing, name="show-listing"),
    path("user_watchlist", views.user_watchlist, name="user-watchlist"),
    path("watchlist/<int:pk>", views.watchlist, name="watchlist"),
    path("bid/<int:pk>", views.new_bid, name="new-bid"),
    path("close_listing/<int:pk>", views.close_listing, name="close-listing"),
]
