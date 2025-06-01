import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=20, blank=False, null=False)
    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null=False)
    password = models.CharField(max_length=20, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Conversation(models.Model):
    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    participants = models.ManyToManyField("User", related_name="converstions")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"conversations {self.participants}"


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="messages"
    )
    conversation = models.ForeignKey(
        "Conversation", on_delete=models.CASCADE, related_name="messages"
    )
    message_ody = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} at {self.sent_at}"
