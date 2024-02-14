from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return obj == request.user
        return obj.user == request.user
