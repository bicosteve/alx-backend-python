from django.apps import AppConfig


class ChatsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_chat"

    def ready(self):
        import django_chat.signals
