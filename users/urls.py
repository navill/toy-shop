from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from users import views

app_name = 'users'

urlpatterns = [
    path("join/", views.UserCreateAPIView.as_view(), name="join"),
    path("login/", TokenObtainPairView.as_view(), name='login'),
    path("<uuid:uuid>/", views.UserRetrieveAPIView.as_view(), name="retrieve"),
    path("<uuid:uuid>/update/", views.UserUpdateAPIView.as_view(), name="update")
]
