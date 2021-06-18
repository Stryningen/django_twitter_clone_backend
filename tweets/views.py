from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api_authentication.utils import getUser
from tweets.models import Tweet, TweetLike
from tweets.serializers import (
    TweetSerializer,
    TweetActionSerializer,
    TweetLikeSerializer,
    ReTweetSerializer,
)

from django.conf import settings


# Create your views here.

ACTIONS = settings.TWEET_ACTIONS


class TweetView(APIView):
    def get(self, request, format=None):
        tweets = Tweet.objects.all().order_by("-tweet_created")
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):

        token = request.headers.get("Authorization")
        data = request.data
        user = None

        if token:
            token = token.split(" ")[1]
            user = getUser(token)

        serializer = TweetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tweet_user=user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TweetActionView(APIView):
    def get(self, request, format=None):
        tweets_likes = Tweet.objects.all().order_by("-tweet_created")
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):

        token = request.headers.get("Authorization")

        if token:
            serializer = TweetActionSerializer(data=request.data)
            token = token.split(" ")[1]
            user = getUser(token)
            if serializer.is_valid():
                data = serializer.validated_data

                id = data.get("id")
                action = data.get("action")
                content = data.get("content")

                action_tweet = Tweet.objects.get(pk=id)

                print(action)

                if not action_tweet:
                    return Response(
                        {"error": "tweet not found"}, status=status.HTTP_404_NOT_FOUND
                    )

                if action == "like":
                    query_set = TweetLike.objects.filter(tweet__id=id, user=user)

                    if not query_set:
                        tweet_like_serializer = TweetLikeSerializer(
                            data={"user": user.id, "tweet": action_tweet.id}
                        )
                        if tweet_like_serializer.is_valid():
                            tweet_like_serializer.save()
                            return Response(
                                serializer.data, status=status.HTTP_201_CREATED
                            )

                    deleted_like = query_set.first().delete()

                    return Response(
                        {"message": "tweet unliked", "action": "unlike"},
                        status=status.HTTP_200_OK,
                    )

                if action == "retweet":
                    retweet = Tweet(
                        tweet_user=user, tweet_text=content, tweet_parent=action_tweet
                    )
                    retweet_serializer = ReTweetSerializer(retweet)
                    if retweet_serializer.is_valid():
                        print(retweet_serializer.data)
                        print("success")

                    if not retweet_serializer.is_valid():
                        print(retweet_serializer.errors)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
        )
