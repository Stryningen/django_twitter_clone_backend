from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status

from django.contrib.auth import get_user_model

from api_authentication.serializers import (
    UserSerializer,
    UserFieldSerializer,
    UserSerializerNoPasswordValidation,
)

import datetime

# Create your views here.

User = get_user_model()


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
                {"result": {"message": f"user {username} created"}},
                status=status.HTTP_201_CREATED,
            )

            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )


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

            data = {"username": user.username, "id": user.id, "token": token.key}

            return Response({"result": data}, status=status.HTTP_200_OK)

        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
