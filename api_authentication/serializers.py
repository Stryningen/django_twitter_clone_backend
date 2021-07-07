from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation

User = get_user_model()


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


class UserFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "id"]
