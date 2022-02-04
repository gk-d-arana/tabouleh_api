from django.db import models
import uuid

from user_roles.models import Admin, Customer, DeliveryOperator


class CustomerChatroom(models.Model):
    chatroom_id = models.UUIDField(
        primary_key=True,
        editable=False,
        default= uuid.uuid4
    )
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, related_name="adminchatcustomer")
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return "Chat With Customer {}".format(self.customer.user.username)
    
    
class DeliveryOperatorChatroom(models.Model):
    chatroom_id = models.UUIDField(
        primary_key=True,
        editable=False,
        default= uuid.uuid4
    )
    admin_user = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, related_name="adminchatdeliveryoperator")
    delivery_operator = models.ForeignKey(DeliveryOperator, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return "Chat With DeliveryOperator {}".format(self.delivery_operator.user.username)
    