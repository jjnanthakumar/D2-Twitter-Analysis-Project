"""NLP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import EmailValidationOnForgotPassword

urlpatterns = [
    path('getemails', views.getEmaillist, name='emails'),
    path('getusers', views.getUsersname, name='users'),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('analyze', views.analyze, name='analyze'),
    path('register', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('about', views.about, name='about'),
    path('privacy', views.privacy, name='privacy'),
    path('contact', views.contact, name='contact'),
    path('logout', views.logout, name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             form_class=EmailValidationOnForgotPassword,
             template_name='password_reset.html',
             subject_template_name='password_reset_subject.txt',
             html_email_template_name='registration/html_password_reset_email.html'),
         name='password-reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'
         ),
         name='password_reset_complete')]
