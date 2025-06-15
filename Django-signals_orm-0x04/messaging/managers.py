from django.db import models


class UnreadMessagesManager(models.Model):
    def for_user(self, user):
        return self.get_queryset().filter(receiver=user, read=False)
