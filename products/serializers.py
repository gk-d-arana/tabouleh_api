from user_roles.serializers import CustomerSerializer
from rest_framework import serializers
from .models import *
from user_roles.models import Customer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['ingredient_name', 'ingredient_name_ar']


class MealSerializer(serializers.ModelSerializer):
    meal_category = CategorySerializer(Category)
    meal_offers = OfferSerializer(Offer ,many=True)
    meal_ingredients = IngredientSerializer(Ingredient ,many=True)
    class Meta:
        model = Meal
        fields = "__all__"


class SimpleMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = [
            'meal_name', 'meal_id', 'meal_points', 'meal_name_ar' ,"meal_main_image"
        ]


class MainMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = [
            'meal_name', 'meal_name_ar', 'meal_id', 'meal_description', 'meal_description_ar', 'meal_rating',
            'customer_meal_price', 'supermarket_meal_price', 'agent_meal_price',
            'restaurant_meal_price', 'company_meal_price', "meal_main_image"
        ]


class MealImageSerializer(serializers.ModelSerializer):
    #meal = MealSerializer(Meal)
    class Meta:
        model = MealImage
        fields = [
            'image_id', 'image'
        ]


class CartItemSerializer(serializers.ModelSerializer):
    meal = MealSerializer(Meal)
    class Meta:
        model = CartItem
        fields = "__all__"


class SimpleCartItemSerializer(serializers.ModelSerializer):
    meal = MainMealSerializer(Meal)
    class Meta:
        model = CartItem
        fields = "__all__"



class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(CartItem, many=True)
    cart_owner = CustomerSerializer(Customer)
    class Meta:
        model = Cart
        fields = "__all__"


class SimpleCartSerializer(serializers.ModelSerializer):
    cart_items = SimpleCartItemSerializer(CartItem, many=True)

    class Meta:
        model = Cart
        fields = "__all__"

