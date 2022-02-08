from products.serializers import CartItemSerializer, SimpleCartItemSerializer, CartSerializer, SimpleCartSerializer
from products.models import Cart
from user_roles.serializers import CustomersListSerializer, DeliveryOperatorSerializer, SimpleUserSerializer
from user_roles.models import Customer ,DeliveryOperator
from extras.models import PaymentType
from extras.serializers import PaymentTypeSerializer, AddressSerializer
from rest_framework import serializers
from .models import *


class DeliverySerializer(serializers.ModelSerializer):
    delivery_operator = DeliveryOperatorSerializer(DeliveryOperator)
    class Meta:
        model = Delivery
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    payment_type = PaymentTypeSerializer(PaymentType)
    cart_items = SimpleCartItemSerializer(CartItem, many=True)
    #delivery = DeliverySerializer(Delivery)
    order_address = AddressSerializer(Address)
    ordered_by = CustomersListSerializer(Customer)
    class Meta:
        model = Order
        fields = [
            'id', 'ordered_at', 'pay_home','cart_items','order_note',
            'payment_type', 'lang', 'lat', 'bill', 'order_address', 'ordered_by'
        ]


class SimpleOrderSerializer(serializers.ModelSerializer):
    payment_type = PaymentTypeSerializer(PaymentType)
    #delivery = DeliverySerializer(Delivery)
    class Meta:
        model = Order
        fields = [
            'ordered_at', 'pay_home',
            'payment_type', 'lang', 'lat', 'bill'
        ]
        
class SimpleOrderSerializerForBackup(serializers.ModelSerializer):
    payment_type = PaymentTypeSerializer(PaymentType)
    #delivery = DeliverySerializer(Delivery)
    class Meta:
        model = Order
        fields = [
            'ordered_at', 'pay_home',
            'payment_type', 'lang', 'lat', 'bill'
        ]


class SimpleListOderSerializer(serializers.ModelSerializer):
    payment_type = PaymentTypeSerializer(PaymentType)
    #delivery = DeliverySerializer(Delivery)
    class Meta:
        model = Order
        fields = [
            'ordered_at', 'pay_home',
            'payment_type', 'lang', 'lat', 'bill'
        ]


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['bill']




class CompleteDeliverySerializer(serializers.ModelSerializer):
    delivery_operator = DeliveryOperatorSerializer(DeliveryOperator)
    order = SimpleOrderSerializer(Order)
    class Meta:
        model = Delivery
        fields = "__all__"



class SemiCompleteDeliverySerializer(serializers.ModelSerializer):
    delivery_operator = DeliveryOperatorSerializer(DeliveryOperator)
    order = OrderSerializer(Order)
    
    class Meta:
        model = Delivery
        fields = "__all__"
        



class SimpleDeliverySerializer(serializers.ModelSerializer):
    order = SimpleOrderSerializer(Order)
    class Meta:
        model = Delivery
        fields = [
            "delivery_id", "is_delivered", 
            "is_being_delivered", "order",
            "city", "lang", "lat", "location"   
        ]
        
        
class MyOrderDeliverySerializer(serializers.ModelSerializer):
    order = OrderSerializer(Order)
    class Meta:
        model = Delivery
        fields = [
            "delivery_id", "is_delivered", 
            "is_being_delivered", "order",
            "city", "lang", "lat", "location", "is_reviewed"
        ]
        
        
class OrderReviewSerializer(serializers.ModelSerializer):
    order = OrderSerializer(Order)
    class Meta:
        model = OrderReview
        fields = "__all__"
        
        



class CompDeliveryOperatorSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(User)
    Deliveries = CompleteDeliverySerializer(Delivery, many=True)
    class Meta:
        model = DeliveryOperator
        fields = [
            'delivery_operator_id', 'user', 
            'points', 'online', 'profile_image',
            'phone_number', 'Deliveries'
        ]