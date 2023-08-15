from rest_framework import permissions


class IsStockOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print("IS CALLING THIS?")
        return obj.owner == request.user
