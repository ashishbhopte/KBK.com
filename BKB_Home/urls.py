from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="index"),
    path('saveform/', views.SaveForm, name="saveform"),
]