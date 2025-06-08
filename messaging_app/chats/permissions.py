from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """Only allow participants to access this conversation"""

    def has_permission(self, request, view):
        """Allow only authenticated users to the conversation"""
        return request.user.is_authenticated

    def has_object_permission(self, request, view, object):
        """Check if a user is a participant in the conversation"""
        if request.method in permissions.SAFE_METHODS:
            return object.participants.filter(id=request.user.id).exists()

        # allow write access [PUT, PATCH,DELETE] participants
        return object.participants.filter(id=request.user.id).exists()
