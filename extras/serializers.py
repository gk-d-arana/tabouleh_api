from rest_framework import serializers
from .models import *
from user_roles.serializers import CustomerSerializer, CustomersListSerializer
from user_roles.models import Customer
from products.models import Meal
from products.serializers import MealSerializer, SimpleMealSerializer


class MainValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainValue
        fields = "__all__"
        
        
class CarouselImageerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselImage
        fields = ['carousel_image']


class AboutSerializer(serializers.ModelSerializer):
    carousel_images = CarouselImageerializer(CarouselImage, many=True)
    class Meta:
        model = About
        fields = "__all__"
        
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"
        
class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = "__all__"
        
        
class AddressSerializer(serializers.ModelSerializer):
    #customer = CustomerSerializer(Customer)

    class Meta:
        model = Address
        fields = [
            'area_name', 'street', 'building_no', 'phone_no', "id"
        ]

class PaymentTypeSerializer(serializers.ModelSerializer):
    #customer = CustomerSerializer(Customer)
    class Meta:
        model = PaymentType
        fields = [
            'payment_id', 'payment_provider', 'card_number',
            'card_cvc', 'card_expire_date'
        ]


class RatingSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(Customer)
    # meal_rated = MealSerializer(Meal)
    class Meta:
        model = Rating
        fields = "__all__"


class RatingListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Rating
        fields = [
            "rating_id", "rating_content", "rating_value", 
            "created_at"
        ]   




class SimpleRatingSerializer(serializers.ModelSerializer):
    customer = CustomersListSerializer(Customer)
    # meal_rated = MealSerializer(Meal)
    class Meta:
        model = Rating
        fields = "__all__"




class WishListSerializer(serializers.ModelSerializer):
    meals = SimpleMealSerializer(Meal, many=True)
    #customer = CustomerSerializer(Customer)
    class Meta:
        model = WishList
        fields = ["meals"]


