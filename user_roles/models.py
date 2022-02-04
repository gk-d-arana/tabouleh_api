from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django_countries.fields import CountryField
from location_field.models.plain import PlainLocationField
from phonenumber_field.modelfields import PhoneNumberField


User = get_user_model()

class Admin(models.Model):
    admin_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    profile_image = models.FileField(null=True, blank=True, upload_to="static/images")
    country = CountryField()
    phone_number = PhoneNumberField(null=True)
    role = models.CharField(default="Admin", max_length=20)
    online = models.BooleanField(default=True)

    def __str__(self):
        return "Admin {}".format(self.user.username)


CUSTOMER_CHOICES = (
    ('NormalCustomer', 'NormalCustomer'),
    ('RestaurantCustomer', 'RestaurantCustomer'),
    ('SuperMarketCustomer', 'SuperMarketCustomer'),
    ('AgentCustomer', 'AgentCustomer'),
    ('CompanyCustomer', 'CompanyCustomer'),
)

class Customer(models.Model):
    customer_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.FloatField(default=0)
    country = CountryField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    profile_image = models.FileField(null=True, blank=True, upload_to="static/images")
    role = models.CharField(default="NormalCustomer", choices=CUSTOMER_CHOICES, max_length=40)
    #  location = PlainLocationField(zoom=7, default="1512142")
    phone_number = PhoneNumberField(null=True)
    addresses = models.ManyToManyField('extras.Address', blank=True, related_query_name="customer_addresses"
        , related_name="customer_addresses"
    )
    online = models.BooleanField(default=True)
    
    def __str__(self):
        return "Customer {}".format(self.user.username)





class DeliveryOperator(models.Model):
    delivery_operator_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    points = models.FloatField(default=0)
    Deliveries = models.ManyToManyField('orders.Delivery', blank=True)
    country = CountryField()
    role = models.CharField(default="DeliveryOperator", max_length=20)
    profile_image = models.FileField(null=True, blank=True, upload_to="static/images")
    online = models.BooleanField(default=True)
    delivering = models.BooleanField(default=False)
    phone_number = PhoneNumberField(null=True)

    def __str__(self):
        return "Delivery Operator {}".format(self.user.username)


class CodesForPassReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="code_for_user")
    code = models.PositiveIntegerField(default=0000)