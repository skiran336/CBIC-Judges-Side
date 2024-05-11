from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.signin, name="signin"),
    path('home', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signout', views.signout, name="signout"),
    path('forgot_password', views.signup, name="forgot_password"),
    path('scorepage', views.scorepage, name="scorepage"),
    path('forgot_password/', auth_views.PasswordResetView.as_view(template_name='authentication/password_reset_form.html'), name='forgot_password'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'), name='password_reset_complete'),

]