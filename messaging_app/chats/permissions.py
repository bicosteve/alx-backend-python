from rest_framework import permissions


class IsPermittedToConverse(permissions.BasePermission):
    """Only allow participants to access this conversation"""

    def has_permission(self, request, view):
        """Allow only authenticated users to the conversation"""
        return request.user.is_authenticated

    def has_object_permission(self, request, view, object):
        """Check if a user is a participant in the conversation"""
        return object.participants.filter(id=request.user.id).exists()
