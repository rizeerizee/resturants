from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    # login and register
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),

    # information
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # customer action
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_food/', views.updateFood, name='update_food'),
    path('submit_order/', views.orderSubmit, name='submit_order'),
    path('feedback/', views.feedBack, name='feedback'),

    # admin action
    path('addfood/', views.addFood, name='addfood'),
    path('editfood/<str:pk>/', views.editFood, name='editfood'),
    path('deletefood/<str:pk>/', views.deleteFood, name='deletefood'),
    path('order/', views.orderPage, name='order'),
    path('finish/<str:pk>/', views.finish, name='finish'),



]