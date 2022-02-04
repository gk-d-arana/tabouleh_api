from django.urls import path
from .views import *


urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('meals/', MealListView.as_view()),
    path('meal_management/', MealManagmentView.as_view()),
    path('category_management/', CategoryManagmentView.as_view()),
    path('delete_all_categories/', delete_all_categories),
    path('category_meals/', CatregoryMealsListView.as_view()),
    path("meal/<str:meal_id>/", MealDetailsView.as_view()),
    path('cart/', CartView.as_view()),
    path('add_to_cart/', add_to_cart),
    path('remove_from_cart/', remove_from_cart),
    path('increase_meal_amount/', increase_meal_amount),
    path('decrease_meal_amount/', decrease_meal_amount),
    path('customer_points/', customer_points),
    #path('edit_category/', edit_category), # add edit = 0 and remove = 1
    path('search/', search, name="search"),
    path('offer_management/', OfferMangmentView.as_view()),
    #Admin Panel
    path('home/', HomeView.as_view()),
    path('add_meal/', add_meal, name="add_meal"),
    path('add_category/', add_category, name="add_category"),
]