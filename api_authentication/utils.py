from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


def getUser(token):
    current_token = Token.objects.filter(key=token).first()
    if current_token:
        return current_token.user

    return None
