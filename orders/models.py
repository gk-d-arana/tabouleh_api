from django.db import models
import uuid
from extras.models import Address
from products.models import *
from user_roles.models import *
from location_field.models.plain import PlainLocationField




class Order(models.Model):
    order_id = models.UUIDField(
         default = uuid.uuid4,
         editable = False)
    ordered_by = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    ordered_at = models.DateTimeField(auto_now_add=True)
    cart_items = models.ManyToManyField(CartItem, blank=True)
    pay_home = models.BooleanField(default=False)
    payment_type = models.ForeignKey('extras.PaymentType', on_delete=models.SET_NULL, blank=True , null=True)  
    delivery = models.ForeignKey('Delivery', on_delete=models.CASCADE, blank=True, null=True, related_name="delivery")
    destination = PlainLocationField(based_fields=['city'], zoom=7, default="0")
    lang = models.CharField(default="0", max_length=255)
    lat = models.CharField(default="0", max_length=255)
    order_address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True, related_name="order_address")
    bill = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)
    order_note = models.TextField(null=True, default="")

    def __str__(self):
        return "Order For {}".format(self.ordered_by.user.username)

    def get_bill(self):
        if self.ordered_by.role == "1": 
            return self.cart.get_customer_total_price()
        elif self.ordered_by.role == "2":
            return self.cart.get_restuarant_total_price()
        elif self.ordered_by.role == "3":
            return self.cart.get_supermarket_total_price()
        elif self.ordered_by.role == "4":
            return self.cart.get_agent_total_price()
        elif self.ordered_by.role == "5":
            return self.cart.get_company_total_price() 
    
    
    def set_bill(self):
        if self.ordered_by.role == "1":
            self.bill = self.cart.get_customer_total_price()
        elif self.ordered_by.role == "2":
            self.bill = self.cart.get_restuarant_total_price()
        elif self.ordered_by.role == "3":
            self.bill = self.cart.get_supermarket_total_price()
        elif self.ordered_by.role == "4":
            self.bill = self.cart.get_agent_total_price()
        elif self.ordered_by.role == "5":
            self.bill = self.cart.get_company_total_price() 




    
    

DELIVERY_REPORT_CHOICES = (
    ('test', 'test'),
    ('test2', 'test2'),
    ('test3', 'test3'),
)


class OrderReview(models.Model):
    review_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    package_review = models.FloatField(default=0.0)
    delivery_review = models.FloatField(default=0.0)
    comment = models.TextField(null=True, default="")





class Delivery(models.Model):
    delivery_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    delivery_operator = models.ForeignKey(DeliveryOperator, on_delete=models.SET_NULL, blank=True, null=True)
    delivery_report = models.TextField(default="Some Problem Occured")
    delivery_problem_report_choice = models.CharField(max_length=255, blank=True,choices=DELIVERY_REPORT_CHOICES)
    is_delivered = models.BooleanField(default=False)
    is_being_delivered = models.BooleanField(default=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE ,related_name="order_for_delivery", null=True)
    city = models.CharField(max_length=255, default="USA")
    location = PlainLocationField(based_fields=['city'], zoom=7, default="0")
    lang = models.CharField(default="0", max_length=255)
    is_reviewed = models.BooleanField(default=False)
    lat = models.CharField(default="0", max_length=255)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    
    class Meta: 
        verbose_name = "Delivery"
        verbose_name_plural = "Deliveries"

