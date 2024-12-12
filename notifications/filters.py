from .models import UserNotification

class NotificationFilter:

    @staticmethod
    def filter_notifications(user, filters):

        notifications = UserNotification.objects.filter(user=user)

        if filters.get('status') is not None:
            notifications = notifications.filter(status=filters['status'])

        if filters.get('notification_type') is not None:
            notifications = notifications.filter(notification_type=filters['notification_type'])

        if filters.get('notification_category') is not None:
            notifications = notifications.filter(
                notification_template__notification_category__id=filters['notification_category']
            )

        return notifications