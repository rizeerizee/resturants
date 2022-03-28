from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Customer, Food, Category, Order, OrderFood, ShippingAddress, Contact, Feedback, Notified, User

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    exclude = []
    list_display = ['customer', 'complete']
    list_display_links = ['customer', 'complete']
    list_filter = ['complete', 'created']
    search_fields = ['id']
    ordering = ['-created']


class MyUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'date_join', 'last_login', 'is_admin', 'is_staff']
    list_display_links = ['username', 'email']
    list_filter = ['date_join']
    search_fields = ['email', 'username']
    ordering = ['id']

class OrderFoodAdmin(admin.ModelAdmin):
    exclude = []
    list_display = ['order', 'food', 'quantity']
    list_display_links = ['order', 'food', 'quantity']
    list_filter = ['order', 'created']
    ordering = ['-created']

class FoodAdmin(admin.ModelAdmin):
    exclude = []
    list_display = ['name', 'price', 'category']
    list_display_links = ['name', 'price', 'category']
    list_filter = ['category', 'created']
    ordering = ['-created']

class CustomerAdmin(admin.ModelAdmin):
    exclude = []
    list_display = ['user', 'name', 'email', 'phone']
    list_display_links = ['user', 'name', 'email', 'phone']
    list_filter = ['user', 'created']
    ordering = ['-created']

class AddressAdmin(admin.ModelAdmin):
    exclude = []
    list_display = ['order', 'name', 'email', 'address', 'phone']
    list_display_links = ['order', 'name', 'email', 'address', 'phone']
    list_filter = ['order', 'created']
    ordering = ['-created']

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Category)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderFood, OrderFoodAdmin)
admin.site.register(ShippingAddress, AddressAdmin)
admin.site.register(Contact)
admin.site.register(Feedback)
admin.site.register(Notified)
admin.site.register(User, MyUserAdmin)
