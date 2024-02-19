from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="Home"),
    path('saveform/', views.SaveForm, name="saveform"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
    path('activate/<slug>', views.activate, name="activate"),

]