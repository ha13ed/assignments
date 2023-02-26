from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("new_page", views.new_page, name="new_page"),
    path("random_page", views.random_page, name="random_page"),
    path("wiki/<str:q>", views.entry, name="entry"),
    path("edit/<str:q>", views.edit_page, name="edit_page"),
]
