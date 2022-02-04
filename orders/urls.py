from django.urls import path
from django.urls.conf import include
from .views import *


from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('unoccupied_deliveries', UnoccupiedDeliveries, basename='unoccupied_deliveries')

urlpatterns = [
    path('submit_order/', submit_order),
    path('submit_single_order/', submit_single_order),
    
    path('order/', OrderRetrieveView.as_view()),
    path('order_as_admin/', AdminOrderRetrieveView.as_view()),
    path('order_as_customer/', CustomerOrderRetrieveView.as_view()),
    path('delivery_details/<str:delivery_id>/', DeliveryRetrieveView.as_view()),
    path('start_delivery/', start_delivery),
    path('admin_start_delivery/', admin_start_delivery),
    path('end_delivery/', end_delivery),
    path('update_location/', update_location),
    path('my_orders/', MyOrders.as_view()),
    path('add_order_review/', add_order_review),
    path('my_orders_reviews/', my_orders_reviews),
    path('my_deliveries/', MyDeliveries.as_view()), 
    path('', include(router.urls))
]
