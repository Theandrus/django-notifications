import django_filters
from notifications.models import UserNotification

class UserNotificationFilter(django_filters.FilterSet):
    status = django_filters.NumberFilter(field_name='status', label='Status')
    notification_type = django_filters.NumberFilter(field_name='notification_type', label='Notification Type')
    notification_category = django_filters.NumberFilter(
        field_name='notification_template__notification_category__id', label='Notification Category'
    )

    class Meta:
        model = UserNotification
        fields = ['status', 'notification_type', 'notification_category']

