from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class TweetLike(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user = self.user or ""
        tweet = self.tweet or ""
        return f"<TweetLike(user: {self.user.username}, tweet id: {tweet.id})>"


class Tweet(models.Model):

    tweet_user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="tweet"
    )
    tweet_text = models.TextField(blank=True, null=True)
    tweet_image = models.ImageField(blank=True, null=True)

    tweet_created = models.DateTimeField(auto_now_add=True)
    tweet_updated = models.DateTimeField(auto_now=True)

    tweet_parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    tweet_likes = models.ManyToManyField(
        User, related_name="tweet_like_user", through=TweetLike, blank=True
    )

    def __str__(self):
        return (
            f"id: {self.id}, text: '{self.tweet_text}', image: {bool(self.tweet_image)}"
        )

    class Meta:
        ordering = ["tweet_created"]
