from rest_framework import serializers


from chats.models import User, Conversation, Message


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = "__all__"


class MessageSerializer(serializers.Serializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = "__all__"


class ConversationSerialzer(serializers.Serializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = "__all__"
