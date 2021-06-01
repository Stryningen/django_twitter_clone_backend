from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api_authentication.utils import getUser
from tweets.models import Tweet
from tweets.serializers import TweetSerializer

# Create your views here.


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
