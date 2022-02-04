from extras.models import Address
from orders.models import Delivery
from user_roles.models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()



class AddressSerializer(serializers.ModelSerializer):
    #customer = CustomerSerializer(Customer)
    class Meta:
        model = Address
        fields = [
            'area_name', 'street', 'building_no', 'phone_no'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'is_staff']


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']




class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer(User)
    class Meta:
        model = Admin
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(User)
    addresses = AddressSerializer(Address, many=True)
    class Meta:
        model = Customer
        fields = '__all__'


class CustomersListSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(User)
    class Meta:
        model = Customer
        fields = [
            'user', 'customer_id', 'profile_image', 'role',
            'phone_number'
        ]




class FullDeliveryOperatorSerializer(serializers.ModelSerializer):
    user = UserSerializer(User)
    class Meta:
        model = DeliveryOperator
        fields = [
            'delivery_operator_id', 'user', 
            'points', 'online', 'profile_image',
            'phone_number'
        ]

class DeliveryOperatorSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(User)
    
    class Meta:
        model = DeliveryOperator
        fields = [
            'delivery_operator_id', 'user', 
            'points', 'online', 'profile_image',
            'phone_number'
        ]



class DeliveryOperatorsListSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(User)
    class Meta:
        model = DeliveryOperator
        fields = [
            'delivery_operator_id', 'user', 'created_at', 
            'points', 'country', 'profile_image', 'online',
            'phone_number'
        ]
