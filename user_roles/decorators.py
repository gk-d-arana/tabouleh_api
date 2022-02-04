from users.models import Admin
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework.authtoken.models import Token


def is_admin(token):
    user = Token.objects.get(key=token).user
    try:       
        admin = Admin.objects.get(user=user)
        return admin
    except ObjectDoesNotExist:
        raise PermissionDenied
