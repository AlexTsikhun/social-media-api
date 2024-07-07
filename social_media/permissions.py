from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """
    Read : anyone
    Delete : admin only
    Create, Update : author only
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(obj, "follower") and obj.follower == request.user:
            return obj.follower == request.user

        if hasattr(obj, "followee") and obj.followee == request.user:
            return obj.followee == request.user

        return obj.user == request.user
