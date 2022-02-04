from django.urls import path
from .views import *

urlpatterns = [
    path("login/", login_view, name="login_view"),
    path("dashboard/", home_view, name="home_view"),
    path("products/", product_view, name="product_view"),
    path("tables/", tables_view, name="tables_view"),
    path("users/", users_view, name="users_view"),
    path("employees/", employees_view, name="employees_view"),
    path("chat/", chat_view, name="chat_view"),
    path("accounts/", accounts_view, name="accounts_view"),
    path("notifications/", notifications_view, name="notifications_view"),
    path('logout_view/', logout_view, name="logout_view"),
]
