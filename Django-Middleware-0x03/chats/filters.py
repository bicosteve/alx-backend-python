import django_filters

from .models import Message, Conversation


class MessageFilter(django_filters.FilterSet):
    """Filters messages"""

    user = django_filters.CharFilter(
        field_name="user__useranme", lookup_expr="icontains"
    )
    start_date = django_filters.DateFilter(field_name="created_at", lookup_expr="gte")
    end_date = django_filters.DateFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Message
        fields = ["user", "start_date", "end_date"]
