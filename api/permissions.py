from rest_framework import permissions
from api.models import Owner
from rest_framework.exceptions import ValidationError


class IsStockOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsUserOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return Owner.objects.get(user=request.user)
        except:
            raise ValidationError("Authenticated User is Not a Owner!")
