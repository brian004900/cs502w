from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createl", views.createl, name="createl"),
    path("inpage/<str:id>", views.inpage, name="inpage"),
    path("addbid/<str:id>", views.addbid, name="addbid"),
    path("addcomment/<str:id>", views.addcomment, name="addcomment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchadd/<str:id>", views.watchadd, name="watchadd"),
    path("categories", views.categories, name="categories"),
    path("incategories/<str:name>", views.incategories, name="incategories"),
]

