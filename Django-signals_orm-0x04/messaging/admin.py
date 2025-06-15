from django.contrib import admin

from .models import Message, Notification, MessageHistory

# Register your models here.
admin.sites.register(Message)
admin.sites.register(Notification)
admin.sites.register(MessageHistory)
