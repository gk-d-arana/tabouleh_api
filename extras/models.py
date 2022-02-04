from products.models import Meal
from django.db import models
from user_roles.models import Customer
import uuid
from phonenumber_field.modelfields import PhoneNumberField
# from phone_field import PhoneField



class About(models.Model):
    company_name = models.CharField(default="", max_length=255, blank=True, null=True)
    company_name_ar = models.CharField(default="", max_length=255, blank=True, null=True)
    company_subtitle = models.CharField(default="", max_length=255, blank=True, null=True)
    company_subtitle_ar = models.CharField(default="", max_length=255, blank=True, null=True)
    company_location = models.CharField(default="", max_length=255, blank=True, null=True)
    company_location_ar = models.CharField(default="", max_length=255, blank=True, null=True)
    company_email= models.EmailField(default="test@gmail.com", max_length=255, blank=True, null=True)
    company_phone_number = models.CharField(default="", max_length=255, blank=True, null=True)
    company_facebook_link = models.CharField(default="", max_length=255, blank=True, null=True)
    company_instagram_link = models.CharField(default="", max_length=255, blank=True, null=True)
    company_description = models.TextField(default="", blank=True, null=True)
    company_description_ar = models.TextField(default="", blank=True, null=True)
    company_features = models.TextField(default="", blank=True, null=True)
    company_features_ar = models.TextField(default="", blank=True, null=True)
    carousel_images = models.ManyToManyField('CarouselImage', related_name="carousel_images", blank=True)
    def __str__(self):
        return self.company_name
    
    
class Service(models.Model):
    our_services = models.TextField(default="", blank=True, null=True)
    our_services_ar = models.TextField(default="", blank=True, null=True)
    

class Agency(models.Model):
    agency_name = models.CharField(max_length=255 ,blank=True, null=True)
    agency_name_ar = models.CharField(max_length=255 ,blank=True, null=True)
    agency_subtitle = models.CharField(max_length=255 ,blank=True, null=True)
    agency_subtitle_ar = models.CharField(max_length=255 ,blank=True, null=True)
    agency_description = models.TextField(max_length=255 ,blank=True, null=True)
    agency_description_ar = models.TextField(max_length=255 ,blank=True, null=True)
    agency_image = models.FileField(upload_to="static/images", blank=True, null=True)    
    
    def __str__(self):
        return self.agency_name
    
"""     class Meta:
        plural_verbose_name = "Agencies" """
    
    

class CarouselImage(models.Model):
    carousel_image = models.FileField(upload_to="static/images", blank=True, null=True)
    
    
class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE ,related_name="customer_address")
    area_name = models.CharField(max_length=255, default="")
    street = models.CharField(max_length=255, default="")
    building_no = models.CharField(max_length=255, default="")
    phone_no = PhoneNumberField(null=True)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    
    # phone_no = PhoneField()
    def __str__(self):
        return "Address For Customer {}".format(self.customer.user.username)

    class Meta:
        verbose_name_plural = "Addresses"



PROVIDER_CHOICES = (
    ("Visa", "Visa"),
    ("Master Card", "Master Card"),
    ("Zein Cash", "Zein Cash"),
)



class PaymentType(models.Model):
    payment_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    payment_provider =  models.CharField(
        max_length = 20,
        choices = PROVIDER_CHOICES,
        default = 'Visa'
        )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    card_cvc = models.PositiveIntegerField(default=123)
    card_expire_date = models.DateField(default="1999-01-01")

    def __str__(self):
        return "Payment Type {} For Customer {}".format(self.payment_provider, self.customer.user.username)


class Rating(models.Model):
    rating_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating_content = models.TextField()
    rating_value = models.FloatField(default=0)
    meal_rated = models.ForeignKey(Meal, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return "Rating For Customer {} For Meal {}".format(self.customer.user.username, self.meal_rated.meal_name)



class WishList(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    meals = models.ManyToManyField(Meal, blank=True)

    def __str__(self):
        return "Wishlist For Customer {}".format(self.customer.user.username)
    
    
class MainValue(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(default="", blank=True, null=True)
    
    def __str__(self):
        return self.name