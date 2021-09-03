from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL


class Friend(models.Model):

    profile_1 = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, related_name="profile_profile_friends"
    )
    profile_2 = models.ForeignKey("Profile", on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"<Friends(:Username {self.profile_1.user.username}, is friends with: {self.profile_2.user.username})"


class Follower(models.Model):

    follower = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, related_name="profile_profile_follower"
    )
    following = models.ForeignKey("Profile", on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"<Follower(follower: {self.follower.profile_user.username}, following: {self.following.profile_user.username})"


class Profile(models.Model):

    profile_user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True
    )
    profile_bio = models.TextField(blank=True)
    profile_created = models.DateTimeField(auto_now_add=True)
    profile_updated = models.DateTimeField(auto_now=True)
    profile_followers = models.ManyToManyField(
        "self", through=Follower, related_name="follower_follower"
    )
    profile_friends = models.ManyToManyField(
        "self", through=Friend, related_name="friend_profile_1"
    )
    profile_block_list = models.ManyToManyField("self", through="Profile")

    def __str__(self):
        return f"<Profile(username: {self.profile_user.username}, user id: {self.profile_user.id})"


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Profile.objects.create(profile_user=instance)
