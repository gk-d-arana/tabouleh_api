from django.urls import path
from .views import *


urlpatterns = [
    path('admin_chat_rooms/', admin_chat_rooms),
    path('customer_chat_rooms/', customer_chat_rooms),
    path('delivery_operator_chat_rooms/', delivery_operator_chat_rooms),
    path('start_customer_chat_room/', start_customer_chat_room),
    path('start_delivery_operator_chat_room/', start_delivery_operator_chat_room),    
]
