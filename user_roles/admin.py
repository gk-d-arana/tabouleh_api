from django.contrib import admin
from .models import *



""" from django.apps import apps
for app_config in apps.get_app_configs():
    for model in app_config.get_models():
        if admin.site.is_registered(model):
            admin.site.unregister(model)
 """


admin.site.register(Admin)
admin.site.register(Customer)
admin.site.register(DeliveryOperator)
admin.site.register(CodesForPassReset)

#  admin.site.register(User)
