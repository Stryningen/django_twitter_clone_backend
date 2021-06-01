from django.contrib.auth.models import User

from rest_framework import serializers

from tweets.models import Tweet


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "id"]


class TweetSerializer(serializers.ModelSerializer):
    tweet_user = UserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = [
            "id",
            "tweet_user",
            "tweet_text",
            "tweet_image",
            "tweet_created",
            "tweet_updated",
        ]
