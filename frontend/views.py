import json
from tkinter import E
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from django.core.exceptions import PermissionDenied
from rest_framework.decorators import api_view
from extras.models import Rating
from products.models import Category, Meal, MealImage, Offer
from user_roles.models import Admin, Customer, DeliveryOperator, User
from orders.models import Order
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        return redirect(home_view)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)    
        except Exception as e:
            raise PermissionDenied
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is not None:
            login(request, user)
            return JsonResponse({'token' : "{}".format(Token.objects.get(user=User.objects.get(username=data['username'])).key)})
        else:
            raise PermissionDenied
    return render(request, 'login.html', {})






@login_required
def home_view(request):
    customers = Customer.objects.order_by('created_at')[:10]
    meals = Meal.objects.order_by('meal_rating')[:10]
    offers = Offer.objects.all()[:10]
    ratings = Rating.objects.all()[:10]
    orders = Order.objects.all()[:10]
    all_categories = Category.objects.all()
    all_meals = Meal.objects.all()
    _meals = []
    for meal in meals:
        meal_images = MealImage.objects.filter(meal=meal).first()
        _meals.append({
            "meal" : meal,
            "meal_images" : meal_images
        })
    return render(request, "home.html", {
        "customers" : customers,
        "meals" : _meals,
        "offers" : offers,
        "ratings" : ratings,
        "orders" : orders,
        "all_categories" : all_categories,
        "all_meals" : all_meals
    })

@login_required
def product_view(request):
    categories = []
    _categories_ = Category.objects.all()
    for category in _categories_:
        categories.append({
            "category" : category,
            "meals" : Meal.objects.filter(meal_category=category),
        })
    return render(request, "products.html", {
        "data" : categories,
        "meal_images" : MealImage.objects.all(),
        "ratings" : Rating.objects.all()
        })


@login_required
def tables_view(request):
    meals = Meal.objects.all()
    return render(request, "tables.html", {"meals" : meals})


@login_required
def users_view(request):
    customers = Customer.objects.all()
    return render(request, "users.html", {"customers" : customers})

@login_required
def employees_view(request):
    delivery_operators = DeliveryOperator.objects.all()
    return render(request, "employees.html", {"delivery_operators" : delivery_operators})

@login_required
def chat_view(request):
    return render(request, "chat.html")

@login_required
def accounts_view(request):
    delivery_operators = DeliveryOperator.objects.all().order_by('-user__date_joined')[:10]
    admins = Admin.objects.all().order_by('-user__date_joined')[:10]
    customers = Customer.objects.all().order_by('-user__date_joined')[:10]
    
    print(delivery_operators)
    return render(request, "accounts.html", {
        "delivery_operators" : delivery_operators,
        "admins" : admins,
        "customers" : customers,
        
        })

@login_required
def notifications_view(request):
    return render(request, "notifications.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


@api_view(['DELETE'])
def delete_user(request, id):
    try:
        admin = Admin.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
    except Exception as e:
        raise PermissionDenied
    user = User.objects.get(id=id) 
    user.delete()
    return JsonResponse({"message" : "success"})   