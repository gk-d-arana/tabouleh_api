from rest_framework import serializers

from chat.models import *


class CustomerChatroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerChatroom
        fields = ["chatroom_id"]
        
        
class DeliveryOperatorChatroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryOperatorChatroom
        fields = ["chatroom_id"]