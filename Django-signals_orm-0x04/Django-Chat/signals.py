from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification_on_new_msg(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        # ensure it is not a new message
        try:
            old_msg = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return

        if old_msg.content != instance.content:
            # save old content to history
            MessageHistory.objects.create(message=instance, old_content=old_msg.content)

            # Set the message as edited
            instance.edited = True
