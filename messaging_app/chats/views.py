from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


from rest_framework import viewsets, permissions, status, filters, authentication
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

# from django_filters.rest_framework import DjangoFilterBackend


from chats.serializers import UserSerializer, ConversationSerialzer, MessageSerializer
from chats.models import User, Conversation, Message
from chats.permissions import IsParticipantOfConversation


# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    query = Conversation.objects.all()
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.BasicAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    serializer_class = ConversationSerialzer
    # filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["participants__email"]
    filterset_fields = ["participants"]

    def get_queryset(self, request):
        return Conversation.objects.filter(participants=request.user)

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


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.BasicAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self, request):
        conversation_id = request.query_param.get("conversation")
        return Message.objects.filter(
            conversation_id=conversation_id, participants=self.request.user
        )

    def perform_create(self, request, serializer):
        conversation = serializer.validated_data["conversation"]
        if self.request.user not in conversation.participants.all():
            raise BaseException("Not a participant of a conversation")
        serializer.save(sender=self.request.user)
