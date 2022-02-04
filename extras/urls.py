from django.urls import path
from .views import *

urlpatterns = [
    path('rating/', RatingView.as_view()),
    path('manage_addresses/', manage_addresses), # add or remove or edit
    path('addresses/', AddressListView.as_view()), # add or remove or edit
    path('meal_ratings/', MealRatings.as_view()),
    path('edit_wishlist/', edit_wishlist), # add or remove meal 
    path('wishlist/', WishListView.as_view()),
    path('manage_payment/', ManagePayment.as_view()),
    path('about_view/', about_view),
    path('services_view/', services_view),
    path('agencies_view/', agencies_view),  
    path("main_values/", main_values, name="main_values")
]