from django.urls import path

from frontend.views import delete_user
from .views import *

urlpatterns = [
    path('admin-authenticate/', admin_authenticate),
    path('admin_login/', admin_login, name="admin_login"),
    path('api_admin_login/', api_admin_login),
    path('delivery_login/', delivery_login),
    path('customer_login/', customer_login),
    path('admin_register/', admin_register, name="admin_login"),
    path('delivery_operator_register/', delivery_operator_register),
    path('customer_register/', customer_register),
    path('admin_details/', admin_details, name="admin_details"),
    path('customer_details/', customer_details),
    path('customer_as_admin/', view_customer_as_admin),
   # path('delivery_as_admin/', view_delivery_operator_as_admin),
    path('delivery_operator_details/', delivery_operator_details),
    path('edit_profile/', ProfileView.as_view()),
    path('edit_profile_image/', UpdateProfileImageView.as_view()),
    path('customers/', CustomersListView.as_view()),
    path('customer_details/', CustomerDetails.as_view()), # get / delete
    path('delivery_operators/', DeliveryOperatorListView.as_view()),
    path('admin_delivery_operator_details/', DelievryOperatorDetails.as_view()), # get / delete
    path('reset_password/', reset_password),
    path('check_code/', check_code),
    path('delete_user/<int:id>/', delete_user),
    path('cp_delivery_operator_register/', cp_delivery_operator_register),
    path('cp_customer_register/', cp_customer_register),
    path("get_profile_image/", get_profile_image, name="get_profile_image"),
]