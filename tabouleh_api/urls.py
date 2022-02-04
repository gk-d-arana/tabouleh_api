from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.shortcuts import render



urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('', include('user_roles.urls')),
    path('', include('products.urls')),
    path('', include('orders.urls')),
    path('', include('extras.urls')), 
    path('', include('chat.urls')), 
    
    path('control_panel/', include('frontend.urls'), name="frontend")  

]




admin.site.site_header = 'TABOULEH'
admin.site.site_title = 'TABOULEH Control Panel'
admin.site.index_title = ''
