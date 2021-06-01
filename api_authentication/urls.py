from django.urls import path

from api_authentication import views

urlpatterns = [
    path("user/create/", views.UserView.as_view()),
    path("user/token/", views.CustomAuthTokenView.as_view()),
]
