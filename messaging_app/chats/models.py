from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)

    def __str__(self):
        return self.username


class Conversation(models.Model):
    participants = models.ManyToManyField("User", related_name="converstions")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"conversations {self.participants}"


class Message(models.Model):
    sender = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="messages"
    )
    conversation = models.ForeignKey(
        "Conversation", on_delete=models.CASCADE, related_name="messages"
    )
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} at {self.timestamp}"
