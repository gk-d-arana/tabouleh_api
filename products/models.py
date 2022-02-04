from django.db import models
import uuid
from user_roles.models import *

class Meal(models.Model):
    meal_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    meal_name = models.CharField(max_length=255)
    meal_name_ar = models.CharField(max_length=255, default="")
    meal_description = models.TextField()
    meal_description_ar = models.TextField(default="") 
    meal_category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name="Category")
    customer_meal_price = models.PositiveIntegerField(default=0)
    supermarket_meal_price = models.PositiveIntegerField(default=0)
    agent_meal_price = models.PositiveIntegerField(default=0)
    restaurant_meal_price = models.PositiveIntegerField(default=0)
    company_meal_price = models.PositiveIntegerField(default=0)
    meal_points = models.FloatField(default=0.0)
    # meal_image_set = models.ManyToManyField('MealImage', related_name="meal_images")
    meal_rating = models.FloatField(default=0)
    meal_offers = models.ManyToManyField('Offer', related_name="meal_offers", blank=True)
    meal_ingredients = models.ManyToManyField('Ingredient', related_name="meal_ingredients", blank=True)
    meal_order_times = models.PositiveIntegerField(default=0)
    meal_main_image = models.FileField(null=True, upload_to="static/images", blank=True)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return self.meal_name


class MealImage(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    image = models.FileField(upload_to="static/images/")
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    
    image_id = models.UUIDField(
     primary_key = True,
     default = uuid.uuid4,
     editable = False)
    def __str__(self):
        return "Image For {}".format(self.meal.meal_name)


class Category(models.Model):
    category_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    category_name = models.CharField(max_length=255)
    category_name_ar = models.CharField(max_length=255, default="")
    category_image = models.FileField(upload_to="static/images", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    meals_count = models.PositiveIntegerField(default=0,blank=True, null=True)
    
    
    def __str__(self):
        return self.category_name

    class Meta: 
        verbose_name = "Category"
        verbose_name_plural = "Categories"


CUSTOMER_CHOICES = (
    ('NormalCustomer', 'NormalCustomer'),
    ('RestaurantCustomer', 'RestaurantCustomer'),
    ('SuperMarketCustomer', 'SuperMarketCustomer'),
    ('AgentCustomer', 'AgentCustomer'),
    ('CompanyCustomer', 'CompanyCustomer'),
)

class Offer(models.Model):
    offer_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    offer_name = models.CharField(max_length=255)
    offer_name_ar = models.CharField(max_length=255, default="")
    normal_customer_offer_price = models.PositiveIntegerField(default=0)
    supermarket_customer_offer_price = models.PositiveIntegerField(default=0)
    agent_customer_offer_price = models.PositiveIntegerField(default=0)
    company_customer_offer_price = models.PositiveIntegerField(default=0)
    restuarant_customer_offer_price = models.PositiveIntegerField(default=0)
    normal_customer_offer_description = models.TextField(null=True, default="")
    supermarket_customer_offer_description = models.TextField(null=True, default="")
    agent_customer_offer_description = models.TextField(null=True, default="")
    company_customer_offer_description = models.TextField(null=True, default="")
    restuarant_customer_offer_description = models.TextField(null=True, default="")
    
    #Arabic
    
    normal_customer_offer_description_ar = models.TextField(null=True, default="")
    supermarket_customer_offer_description_ar = models.TextField(null=True, default="")
    agent_customer_offer_description_ar = models.TextField(null=True, default="")
    company_customer_offer_description_ar = models.TextField(null=True, default="")
    restuarant_customer_offer_description_ar = models.TextField(null=True, default="")
    
    offer_image = models.FileField(null=True, upload_to="static/images")
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Offer {} For Meal {}".format(self.offer_name, self.meal.meal_name)
    
    class Meta: 
        verbose_name = "Offer"
        verbose_name_plural = "Offers"


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=255)
    ingredient_name_ar = models.CharField(max_length=255, default="")
    def __str__(self):
        return self.ingredient_name
    

class CartItem(models.Model):
    cart_item_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    cart_item_owner = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="cart_item_owner")

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "Cart Item For Meal {} For Customer {}".format(self.meal.meal_name, self.cart_item_owner.user.username)
    
    def get_point_count(self):
        return self.meal.meal_points

    def get_customer_meal_item_total_price(self):
        return self.meal.customer_meal_price * self.quantity 

    def get_supermarket_meal_total_price(self):
        return self.meal.supermarket_meal_price * self.quantity 

    def get_agent_meal_total_price(self):
        return self.meal.agent_meal_price * self.quantity 

    def get_restaurant_meal_total_price(self):
        return self.meal.restaurant_meal_price * self.quantity 

    def get_company_meal_total_price(self):
        return self.meal.company_meal_price * self.quantity 


class Cart(models.Model):
    cart_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    cart_owner = models.ForeignKey(Customer, on_delete=models.CASCADE ,related_name="cart_owner")
    cart_items = models.ManyToManyField(CartItem, blank=True)

    def __str__(self):
        return "{} Cart".format(self.cart_owner)

    def get_total_points(self):
        total_points = 0
        for cart_item in self.cart_items.all():
            total_points += cart_item.get_point_count()
        return total_points

    def get_customer_total_price(self):
        total_price = 0
        for cart_item in self.cart_items.all():
            total_price += cart_item.get_customer_meal_item_total_price()
        return total_price


    def get_supermarket_total_price(self):
        total_price = 0
        for cart_item in self.cart_items.all():
            total_price += cart_item.get_supermarket_meal_total_price()
        return total_price

    def get_agent_total_price(self):
        total_price = 0
        for cart_item in self.cart_items.all():
            total_price += cart_item.get_agent_meal_total_price()
        return total_price

    def get_restuarant_total_price(self):
        total_price = 0
        for cart_item in self.cart_items.all():
            total_price += cart_item.get_restaurant_meal_total_price()
        return total_price

    def get_company_total_price(self):
        total_price = 0
        for cart_item in self.cart_items.all():
            total_price += cart_item.get_company_meal_total_price()
        return total_price


