from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.signin, name="signin"),
    path('home', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signout', views.signout, name="signout"),
    path('forgot_password', views.signup, name="forgot_password"),
    path('scorepage', views.scorepage, name="scorepage"),
    path('save_data', views.save_data, name="save_data")

   
]