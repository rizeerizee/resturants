from dataclasses import field
import django
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Food
from .models import User

class CreateUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'username', 'password1', 'password2']

class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = '__all__'

    