
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:id>", views.profile, name="profile"),
    path("follow/<str:id>", views.follow, name="follow"),
    path("unfollow/<str:id>", views.unfollow, name="unfollow"),
    path("edit/<str:post_id>", views.edit, name="edit_post"),
    path("like/<str:post_id>", views.like, name="like")
]
