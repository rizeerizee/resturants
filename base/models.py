from contextlib import nullcontext
from email.policy import default
from re import L
from tkinter import N
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('User must have email!')
        if not username:
            raise ValueError('User must have username!')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True, unique=True)
    date_join = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    object = MyUserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    avatar = models.ImageField(default='testimonial_img1.png', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    @property
    def avaterUrl(self):
        try:
            url = self.avatar.url
        except:
            url = ''
        return url

class Category(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    description = models.TextField(null=True, blank=True)
    discount = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(default='food-1.png', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    translation_id = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def cart_food(self):
        foods = self.orderfood_set.all()
        total = sum([food.quantity for food in foods])
        return total

    @property
    def cart_total(self):
        foods = self.orderfood_set.all()
        total = sum([food.get_total for food in foods])
        return total

class OrderFood(models.Model):
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = (self.food.price * self.quantity)
        return total

class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.address

class Contact(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    subject = models.CharField(max_length=200, null=True)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Feedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.message[0:30]

class Notified(models.Model):
    email = models.EmailField(null=True)

    def __str__(self):
        return self.email
