from django.conf import settings

from rest_framework import serializers

from tweets.models import Tweet, TweetLike
from api_authentication.serializers import UserFieldSerializer

ACTIONS = settings.TWEET_ACTIONS


class TweetCreateSerializer(serializers.ModelSerializer):
    tweet_user = UserFieldSerializer(read_only=True)
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


class TweetSerializer(serializers.ModelSerializer):

    tweet_user = UserFieldSerializer(read_only=True)
    tweet_parent = TweetCreateSerializer(read_only=True)
    tweet_likes = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = [
            "id",
            "tweet_user",
            "tweet_parent",
            "tweet_text",
            "tweet_image",
            "tweet_likes",
            "tweet_created",
            "tweet_updated",
        ]

    def get_tweet_likes(self, tweet):
        return tweet.tweet_likes.count()


class TweetActionSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False, allow_null=True)

    def validate_action(self, action):
        action = action.lower().strip()
        if not action in ACTIONS:
            return serializers.ValidationError("not a valid action")
        return action
