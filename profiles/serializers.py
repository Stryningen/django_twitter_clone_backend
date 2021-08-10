from django.conf import settings
from datetime import datetime

from rest_framework import serializers

from api_authentication.serializers import UserFieldSerializer
from profiles.models import Profile, Follower

ACTIONS = settings.PROFILE_ACTIONS


class ProfileCreateSerializer(serializers.ModelSerializer):
    profile_user = UserFieldSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "profile_user",
            "profile_bio",
            "profile_created",
            "profile_updated",
        ]


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ["follwer", "following", "time_stamp"]


class ProfileSerializer(serializers.ModelSerializer):

    profile_user = UserFieldSerializer(read_only=True)
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "profile_user",
            "profile_bio",
            "profile_created",
            "profile_updated",
            "followers_count",
        ]

    def get_followers_count(self, profile):
        return profile.profile_followers.count()


class ProfileActionSerializer(serializers.Serializer):

    action = serializers.CharField()

    def validate_action(self, action):
        action = action.lower().strip()
        if not action in ACTIONS:
            return serializers.ValidationError("not a valid action")
        return action


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "profile_bio",
        ]
