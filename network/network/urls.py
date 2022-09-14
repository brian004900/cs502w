
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("addpost", views.addpost, name="addpost"),


    #api
    path("loadpost", views.load, name="loadpost"),
    path("paginate", views.paginate, name="paginate"),
    path("paginate/f", views.loadfpost, name="loadfpost"),
    path("show/p/<int:user_id>", views.loadppost, name="loadppost"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("follow/<int:user_id>", views.updatef, name="update_follow"),
    path("post/<int:post_id>", views.updatel, name="update_like"),
  
]

    