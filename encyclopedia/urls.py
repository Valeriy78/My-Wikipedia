from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.article, name="article"),
    path("random", views.random_article, name="random"),
    path("search", views.search, name="search"),
    path("add", views.add, name="add"),
    path("wiki/<str:name>/edit", views.edit, name="edit")
]
