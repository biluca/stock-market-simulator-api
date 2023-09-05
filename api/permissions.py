from rest_framework import permissions
from api.models import User
from rest_framework.exceptions import ValidationError


class IsStockOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

