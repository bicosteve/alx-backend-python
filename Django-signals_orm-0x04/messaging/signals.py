from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import User, Message, Notification, MessageHistory


# message send signal
@receiver(post_save, sender=Message)
def create_notification_on_new_msg(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


# message edit signal
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


@receiver(post_delete, sender=User)
def user_post_delete_cleanup(sender, instance, **kwargs):
    user = instance

    # Delete messeges where the user is sender or receiver
    msgs = Message.objects.filter(sender=user) | Message.objects.filter(reciever=user)
    msg_ids = msgs.values_list("id", flat=True)

    # Delete messages (if not handled by CASCADE)
    msgs.delete()

    # Delete msg edit history
    MessageHistory.objects.filter(editor=user).delete()

    print(f"User {instance.username} histories deleted")
