from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status

from django.contrib.auth.models import User

from api_authentication.serializers import (
    UserSerializer,
    UserSerializerNoPasswordValidation,
)

import datetime

# Create your views here.


class UserView(APIView):
    def post(self, request, format=None):
        username = request.data.get("username")
        password = request.data.get("password")
        ignore_password_validation = request.data.get("ignore_password_validation")
        data = {"username": username, "password": password}

        u = User(username=username)

        serializer = UserSerializer(data=data)
        if ignore_password_validation:
            serializer = UserSerializerNoPasswordValidation(data=data)
        if serializer.is_valid():
            u.set_password(password)
            u.save()
            return Response(
                {"message": f"user {username} created"}, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)

            if not created:
                token.created = datetime.datetime.now()
            user = serializer.validated_data["user"]
            return Response(
                {
                    "token": token.key,
                    "user": user.username,
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
