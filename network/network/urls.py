
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("accounts/<str:username>", views.profile, name="profile"),
    path("following", views.following_index, name="following"),

    #API Routes
    path("create_post", views.create, name="create"),
    path("if_authenticated", views.if_authenticated, name="if_authenticated"),
    path("manage_like", views.manage_like, name="manage_like"),
    path("manage_follow", views.manage_follow, name="manage_follow"),

]
