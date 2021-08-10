from django.urls import path

from profiles import views

urlpatterns = [
    path("<int:profile_id>/", views.ProfileView.as_view()),
    path("", views.ProfileView.as_view()),
]
