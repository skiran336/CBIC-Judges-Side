from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signup', views.signin, name="signin"),
    path('signup', views.signup, name="signout"),

   
]