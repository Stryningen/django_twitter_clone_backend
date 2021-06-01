from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth import password_validation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]

    def validate_password(self, password):
        check_password = password_validation.validate_password(password)
        if not check_password:
            raise serializers.ValidationError(check_password)
        return password


class UserSerializerNoPasswordValidation(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
