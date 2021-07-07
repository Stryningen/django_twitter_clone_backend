from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()


def getUser(token):
    current_token = Token.objects.filter(key=token).first()
    if current_token:
        return current_token.user

    return None
