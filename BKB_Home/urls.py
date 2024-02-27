from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="Home"),
    path('saveform/', views.SaveForm, name="saveform"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
    path('afterlogin/', views.afterlogin, name="afterlogin"),
    path('activate/<slug:auth_tocken>/', views.activate, name="activate"),
    path('resetpassword/<slug:token>/', views.resetpassword, name="resetpassword"),
    path('forgetpassword/', views.forgetpassword, name="forgetpassword"),
    path('changepassword/', views.changepassword, name="changepassword"),

]