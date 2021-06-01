from django.urls import path

from tweets import views

urlpatterns = [
    path("chirps/", views.TweetView.as_view()),
    path("chirps/create/", views.TweetView.as_view()),
]
