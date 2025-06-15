import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UnreadMessagesManager


class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=20, blank=False, null=False)
    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null=False)
    password = models.CharField(max_length=20, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User {self.email}"


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    # self reference for thread msgs
    parent_message = models.ForeignKey(
        "self", mull=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )

    objects = models.Manager()
    unreadMsg = UnreadMessagesManager()

    def __str__(self):
        return f"From {self.sender.email} to {self.receiver.email} snip; {self.content[:30]}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="message"
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} msg - {self.message.message_id}"


class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="history"
    )
    old_content = models.TextField()
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="editor")
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Edit history for message {self.message.message_id} edited at {self.edited_at} edited by {self.edited_by}"
