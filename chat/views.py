from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token
from .serializers import *
from .models import *
import json



@api_view(['GET'])
def admin_chat_rooms(request):
    try:
        admin = Admin.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        chat_rooms_with_customers = CustomerChatroom.objects.filter(admin=admin)
        chat_rooms_with_delivery_operators = DeliveryOperatorChatroom.objects.filter(admin=admin)
        return Response({
            "customers": CustomerChatroomSerializer(chat_rooms_with_customers, many=True).data,
            "delivery_operators": DeliveryOperatorChatroomSerializer(chat_rooms_with_delivery_operators, many=True).data,
            })
    except Exception as e:
        raise PermissionDenied



@api_view(['GET'])
def customer_chat_rooms(request):
    try:
        customer = Customer.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        chat_rooms = CustomerChatroom.objects.filter(customer=customer)
        return Response(
            CustomerChatroomSerializer(chat_rooms, many=True).data
            )
    except Exception as e:
        raise PermissionDenied
    
    
    
@api_view(['GET'])
def delivery_operator_chat_rooms(request):
    try:
        delivery_operator = DeliveryOperator.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        chat_rooms = DeliveryOperatorChatroom.objects.filter(delivery_operator=delivery_operator)
        return Response(
            DeliveryOperatorChatroomSerializer(chat_rooms, many=True).data
            )
    except Exception as e:
        raise PermissionDenied
    
    
    
@api_view(['POST'])
def start_customer_chat_room(request):
    try:
        admin = Admin.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
    except Exception as e:
        raise PermissionDenied
    try:
        data = json.loads(request.body)
        customer = Customer.objects.get(customer_id=data['customer_id'])
        chatroom, created = CustomerChatroom.objects.get_or_create(admin=admin, customer=customer)
        chatroom.save()
        return Response({"message" : "Success", "chatroom_id" : "{}".format(chatroom.chatroom_id)}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"messgae" : "Please Pass Valid Customer Id"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
def start_delivery_operator_chat_room(request):
    try:
        admin = Admin.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
    except Exception as e:
        raise PermissionDenied
    try:
        data = json.loads(request.body)
        delivery_operator = DeliveryOperator.objects.get(delivery_operator_id=data['delivery_operator_id'])
        chatroom, created = DeliveryOperatorChatroom.objects.get_or_create(admin=admin, delivery_operator=delivery_operator)
        chatroom.save()
        return Response({"message" : "Success", "chatroom_id" : "{}".format(chatroom.chatroom_id)}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"messgae" : "Please Pass Valid Customer Id"}, status=status.HTTP_404_NOT_FOUND)
    