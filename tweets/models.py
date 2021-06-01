from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Tweet(models.Model):

    tweet_user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="tweet"
    )
    tweet_text = models.TextField(blank=True, null=True)
    tweet_image = models.ImageField(blank=True, null=True)

    tweet_created = models.DateTimeField(auto_now_add=True)
    tweet_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"id: {self.id}, text: '{self.tweet_text}', image: {bool(self.tweet_image)}"
        )

    class Meta:
        ordering = ["tweet_created"]
