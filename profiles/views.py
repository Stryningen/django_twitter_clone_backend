from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api_authentication.utils import getUser
from profiles.models import Profile, Follower

from profiles.serializers import ProfileSerializer

from django.conf import settings

# Create your views here.


class ProfileView(APIView):
    def get(self, request, format=None, *args, **kwargs):

        if self.kwargs["profile_id"]:
            id = self.kwargs["profile_id"]
            profile = Profile.objects.filter(pk=id).first()
            print(profile)
            if not profile:
                return Response(
                    {"message": "profile not found"}, status=status.HTTP_404_NOT_FOUND
                )
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST
        )

    def post(self, request, format=None):

        token = request.headers.get("Authorization")
        data = request.data
        user = None

        if token:
            token = token.split(" ")[1]
            user = getUser(token)

        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile_user=user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
