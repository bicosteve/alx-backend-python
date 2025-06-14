from django.contrib import admin

from .models import Message, Notification

# Register your models here.
admin.sites.register(Message)
admin.sites.register(Notification)
