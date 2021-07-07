from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, BaseUserManager, AbstractUser

# Create your models here.


class CostumUserManager(BaseUserManager):

    """Basic Manager for CostumUser"""

    def create_user(self, username, password, **extra_fields):
        """
        Creates costum user and sets a auth token.
        """
        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        """
        Creates superuser and sets a auth token.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("superuser must have is_superuser=True")

        return self.create_user(username, password, **extra_fields)


class CostumUser(AbstractUser):

    """Costum user model"""

    objects = CostumUserManager()
    pass


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
