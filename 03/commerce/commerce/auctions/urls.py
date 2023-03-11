from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories_index, name="categories_index"),
    path("categories/<str:q>", views.categories, name="categories"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("closed", views.closed, name="closed"),
]
