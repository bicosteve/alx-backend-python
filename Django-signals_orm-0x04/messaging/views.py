from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

# DRF
from rest_framework import viewsets, permissions, status, authentication
from rest_framework.response import Response
from rest_framework.decorators import action


from .auth import user_can_access_conversation, user_can_access_message
from .filters import MessageFilter
from .pagination import MessagePagination
from messaging.serializers import ConversationSerialzer, MessageSerializer
from .models import User, Conversation, Message
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.user_id)

    def delete_user(self, request, *args, **kwargs):
        user = self.get_boject()

        if user != request.user:
            return Response(
                {"msg": "You only delete your account"}, status.HTTP_400_BAD_REQUEST
            )

        logout(request)
        user.delete()
        return Response({"msg": "Account deleted"}, status.HTTP_204_NO_CONTENT)


class ConversationViewSet(viewsets.ModelViewSet):
    query = Conversation.objects.all()
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.BasicAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    serializer_class = ConversationSerialzer
    search_fields = ["participants__email"]
    filterset_fields = ["participants"]

    def get_queryset(self, request):
        conv_id = self.kwargs.get("pk")
        conversation = super().get_object()

        if not user_can_access_conversation(self.request.user, conv_id):
            return Response(
                {"msg": "You do not have permissions"}, status=status.HTTP_403_FORBIDDEN
            )
        return conversation

    def get_serializer_class(self):
        if self.action == "list":
            return ConversationSerialzer

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    @action(detail=True, methods=["post"])
    def add_participant(self, request, pk=None):
        conversation = self.get_object()
        user_id = request.data.get("user_id")
        user = get_object_or_404(User, pk=user_id)
        conversation.participants.add(user)
        return Response({"msg": "user added"}, status=status.HTTP_201_CREATED)


@method_decorator(cache_page(60), name="dispatch")
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.BasicAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    filter_class = MessageFilter
    pagination_class = MessagePagination
    filterset_class = MessageFilter

    def get_queryset(self, request):
        conversation_id = request.query_param.get("conversation")
        sender = request.user
        message_id = request.query_param.get("message")
        message = (
            Message.objects.filter(receiver=sender, parent_message__isnull=True)
            .select_related("sender", "receiver")
            .prefetch_related("replies__sender", "replies__receiver")
            .get(id=message_id)
        )

        if not user_can_access_message(self.request.user, conversation_id):
            return Response(
                {"msg": "You do not have permissions"}, status=status.HTTP_403_FORBIDDEN
            )

        thread = self.get_thread(message)

        return Response(thread, status.HTTP_200_OK)

    def unread_inbox(self, request):
        user = request.user
        unread_msgs = (
            Message.unread.for_user(user)
            .only("id", "sender", "content", "timestamp")
            .select_related("sender")
        )

        return Response(unread_msgs, status.HTTP_200_OK)

    def perform_create(self, request, serializer):
        conversation = serializer.validated_data["conversation"]
        if self.request.user not in conversation.participants.all():
            raise BaseException("Not a participant of a conversation")
        serializer.save(sender=self.request.user)

    def get_thread(self, msg):
        """Recursively fetch message and its replies"""
        thread = {
            "id": msg.id,
            "content": msg.content,
            "sender": msg.sender.username,
            "timestamp": msg.timestamp,
            "replies": [],
        }

        for reply in (
            msg.replies.all().select_related("sender").prefetch_related("replies")
        ):
            thread["replies"].append(reply)

        return thread
