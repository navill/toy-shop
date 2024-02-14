from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.utils import extend_schema
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@extend_schema(exclude=True)
@api_view()
@permission_classes([AllowAny])
def health_check(request):
    return Response(data={"status": "ok"}, status=status.HTTP_200_OK)


urlpatterns = [
    path("healthcheck/", health_check, name="healthcheck"),
    path("users/", include("users.urls")),
    path("items/", include("items.urls")),
    path("orders/", include("orders.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('docs/ko/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    ]
