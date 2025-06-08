from django.shortcuts import get_list_or_404
from .models import Conversation, Message


def user_can_access_message(user, message_id):
    message = get_list_or_404(Message, id=message_id)
    return message in user.messages.all()


def user_can_access_conversation(user, conversation_id):
    conversation = get_list_or_404(Conversation, id=conversation_id)
    return conversation in user.conversations.all()
