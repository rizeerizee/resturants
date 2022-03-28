from re import sub
from unicodedata import category
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from .models import Contact, Feedback, Food, Customer, ShippingAddress, Order, OrderFood, Notified
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, FoodForm

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import datetime
import json
# Create your views here.

def register(request):
    page = 'login'
    forms = CreateUserForm()
    if request.method == "POST":
        forms = CreateUserForm(request.POST)
        if forms.is_valid():
            user = forms.save()
            Customer.objects.create(
                user=user,
                name=user.username,
                email=user.email,
            )
            return redirect('login')
    context = {'page': page, 'forms': forms}
    return render(request, 'base/register.html', context)

def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password incorrect!')
    context = {'page': page}
    return render(request, 'base/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def home(request):
    special_foods = Food.objects.filter(category__name='Special Dishes')
    top_foods = Food.objects.filter(category__name='Top Dishes')
    breakfasts = Food.objects.filter(category__name='Breakfast')
    lunchs = Food.objects.filter(category__name='Lunch')
    dinners = Food.objects.filter(category__name='Dinner')
    feedbacks = Feedback.objects.all()
    page = 'home'

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    else:
        data = cartCookie(request)
        order = data['order']

    if request.method == 'POST':
        email = request.POST.get('email')
        noti, created = Notified.objects.get_or_create(email=email)
        return redirect('home')


    context = {'page': page, 'special_foods': special_foods, 'top_foods': top_foods, 'breakfasts': breakfasts,
    'lunchs': lunchs, 'dinners': dinners, 'order': order, 'feedbacks': feedbacks}
    return render(request, 'base/index.html', context)

def menu(request):
    special_foods = Food.objects.filter(category__name='Special Dishes')
    top_foods = Food.objects.filter(category__name='Top Dishes')
    breakfasts = Food.objects.filter(category__name='Breakfast')
    lunchs = Food.objects.filter(category__name='Lunch')
    dinners = Food.objects.filter(category__name='Dinner')
    page = 'menu'

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    else:
        data = cartCookie(request)
        order = data['order']
        


    context = {'page': page, 'special_foods': special_foods, 'top_foods': top_foods, 'breakfasts': breakfasts,
    'lunchs': lunchs, 'dinners': dinners, 'order': order}
    return render(request, 'base/menu.html', context)

def about(request):
    page = 'about'
    context = {'page': page}
    return render(request, 'base/about.html', context)

def orderPage(request):
    customer = request.user.customer
    orders = Order.objects.filter(complete=True)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    context = {'orders': orders, 'order': order}
    return render(request, 'base/order_page.html', context)

def contact(request):
    page = 'contact'
    if request.method == "POST":
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        name = first_name + " " + last_name
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )

        return redirect('home')
    context = {'page': page}
    return render(request, 'base/contact.html', context)

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_food = order.orderfood_set.all()
    
    else:
        data = cartCookie(request)
        order_food = data['items']
        order = data['order']


    context = {'order_food': order_food, 'order': order}
    return render(request, 'base/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_food = order.orderfood_set.all()
    
    else:
        data = cartCookie(request)
        order = data['order']
        order_food = data['items']
    context = {'order_food': order_food, 'order': order}
    return render(request, 'base/checkout.html', context)

def updateFood(request):
    data = json.loads(request.body)
    foodId = data['foodId']
    action = data['action']

    customer = request.user.customer

    food = Food.objects.get(id=foodId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_food, created = OrderFood.objects.get_or_create(order=order, food=food)

    

    if action == 'add':
        order_food.quantity += 1
    elif action == 'remove':
        order_food.quantity -= 1

    order_food.save()

    if order_food.quantity <= 0:
        order_food.delete()

    return JsonResponse('Food updated!', safe=False)

def orderSubmit(request):
    data = json.loads(request.body)
    total = float(data['form']['total'])
    form = data['form']
    id = datetime.datetime.now().timestamp()
    addressData = data['addressData']


    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        data = cartCookie(request)
        order = data['order']
        items = data['items']

        name = form['name']
        email = form['email']
        customer, created = Customer.objects.get_or_create(name=name, email=email)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        for item in items:
            food = Food.objects.get(id=item['food']['id'])
            OrderFood.objects.create(order=order, food=food, quantity=item['quantity'])     

    if total == float(order.cart_total):
        ShippingAddress.objects.create(order=order, name=customer,
         email=customer.email, address=addressData['address'],
         phone=addressData['phone'])
        
        order.translation_id = id
        order.complete = True
        order.save()

    return JsonResponse('Order Submited...', safe=False)

def cartCookie(request):

    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'cart_food': 0, 'cart_total': 0}
    
    for i in cart:
        order['cart_food'] += cart[i]['quantity']
        food = Food.objects.get(id=i)
        total = (cart[i]['quantity'] * food.price)
        order['cart_total'] += total

        item = {
            'id': food.id,
            'food': {
                'id': food.id, 'name': food.name, 'price': food.price,
                'imageUrl': food.imageUrl
            },
            'quantity': cart[i]['quantity'], 'get_total': total,
        }

        items.append(item)

    return {'order': order, 'items': items}

@login_required(login_url='login')
def feedBack(request):
    if request.method == 'POST':
        customer = request.user.customer
        message = request.POST.get('message')
        Feedback.objects.create(customer=customer, message=message)
        return redirect('home')
    return render(request, 'base/feedback_form.html')

def addFood(request):
    forms = FoodForm()
    if request.method == 'POST':
        forms = FoodForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('home')

    context = {'forms': forms}
    return render(request, 'base/food_form.html', context)

def editFood(request, pk):
    food = Food.objects.get(id=pk)
    forms = FoodForm(instance=food)
    if request.method == 'POST':
        forms = FoodForm(request.POST, instance=food)
        if forms.is_valid():
            forms.save()
            return redirect('home')

    context = {'forms': forms}
    return render(request, 'base/food_form.html', context)

def deleteFood(request, pk):
    page = 'login'
    food = Food.objects.get(id=pk)
    if request.method == "POST":
        food.delete()
        return redirect('home')
    context = {'obj': food, 'page': page}
    return render(request, 'base/delete.html', context)


def finish(request, pk):
    order = Order.objects.get(id=pk)
    customer = order.customer.name
    customer_email = str(order.customer.email)
    email = EmailMessage(
        'Thank for purchasing the order!',
        customer + "'s order is Finished. Have a nice day! Thank You!",
        settings.EMAIL_HOST_USER,
        [customer_email],
    )
    email.fail_silently = False
    email.send()

    order.delete()

    return redirect('order')





