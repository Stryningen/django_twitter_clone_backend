from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api_authentication.utils import getUser
from profiles.models import Profile, Follower

from profiles.serializers import (
    ProfileSerializer,
    ProfileCreateSerializer,
    ProfileUpdateSerializer,
    FollowerSerializer,
)

from django.conf import settings

# Create your views here.

User = settings.AUTH_USER_MODEL


class ProfileView(APIView):
    def get(self, request, format=None, *args, **kwargs):

        can_edit_profile = False
        token = request.headers.get("Authorization")

        if self.kwargs["profile_id"]:
            id = self.kwargs["profile_id"]

            if token:
                user = getUser(token.split(" ")[1])
                if user.id == id:
                    can_edit_profile = True

            profile = Profile.objects.filter(pk=id).first()
            if not profile:
                return Response(
                    {"errors": [{"message": "profile not found"}]},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = ProfileSerializer(profile)
            return Response(
                {"result": {**serializer.data, "can_edit_profile": can_edit_profile}},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"errors": [{"message": "Something went wrong"}]},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def post(self, request, format=None):

        token = request.headers.get("Authorization")
        data = request.data
        user = None
        can_edit_profile = False

        if token:
            token = token.split(" ")[1]
            user = getUser(token)

            if user.id != int(data["user_id"]) and user.id != data["profile_id"]:
                return Response(
                    {"errors": {"message": "Not authorized"}},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return Response(
                {"errors": {"message": "You are not logged in"}},
                status=status.HTTP_403_FORBIDDEN,
            )

        profile = Profile.objects.filter(profile_user=user).first()
        if profile:
            serializer = ProfileUpdateSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"result": serializer.data},
                    status=status.HTTP_201_CREATED,
                )
        else:
            serializer = ProfileCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(profile_user=user)
                return Response(
                    {"result": serializer.data},
                    status=status.HTTP_201_CREATED,
                )

        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class FollowerView(APIView):
    def get(self, request, format=None):

        token = request.headers.get("Authorization")
        data = request.data

        if not token:
            return Response(
                {"errors": {"token": "token is required"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = token.split(" ")[1]
        user = getUser(token)

        profile_following = Profile.objects.filter(profile_user=user)
        query_set = Follower.objects.filter(following=profile_following)

        serializer = FollowerSerializer(query_set)
        if serializer.is_valid():
            return Response({"result": serializer.data}, status=status.HTTP_200_OK)

        return Response(
            {"errors": {"message": "something went wrong"}},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def post(self, request, format=None):

        token = request.headers.get("Authorization")
        data = request.data
        following_user_id = data["following_id"]

        if not token:
            return Response(
                {"errors": {"message": "You are not authorized"}},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token = token.split(" ")[1]
        follower_user = getUser(token)
        following_user = User.objects.get(pk=following_user_id)
        profile_follower = Profile.objects.filter(profile_user=follower_user)
        profile_following = Profile.objects.filter(profile_user=follower_user)

        query_set = Follower.objects.filter(
            follower=profile_follower, following=profile_following
        )

        serializer_data = {
            "follower": profile_follower,
            "following": profile_following,
        }
        serializer = FollowerSerializer(data=serializer_data)

        # if serializer.is_valid():
