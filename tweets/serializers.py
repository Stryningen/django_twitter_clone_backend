from django.contrib.auth.models import User

from rest_framework import serializers

from tweets.models import Tweet, TweetLike
from django.conf import settings

ACTIONS = settings.TWEET_ACTIONS


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "id"]


class TweetSerializer(serializers.ModelSerializer):
    tweet_user = UserSerializer(read_only=True)
    tweet_likes = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = [
            "id",
            "tweet_user",
            "tweet_text",
            "tweet_image",
            "tweet_likes",
            "tweet_parent",
            "tweet_created",
            "tweet_updated",
        ]

    def get_tweet_likes(self, tweet):
        return tweet.tweet_likes.count()


class TweetLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetLike
        fields = ["user", "tweet", "time_stamp"]


class ReTweetSerializer(serializers.ModelSerializer):

    tweet_user = UserSerializer(read_only=True)
    tweet_parent = TweetSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = [
            "id",
            "tweet_user",
            "tweet_parent",
            "tweet_text",
            "tweet_image",
            "tweet_created",
            "tweet_updated",
        ]


class TweetActionSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False, allow_null=True)

    def validate_action(self, action):
        action = action.lower().strip()
        if not action in ACTIONS:
            return serializers.ValidationError("not a valid action")
        return action
