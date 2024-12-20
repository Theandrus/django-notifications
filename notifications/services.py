from notifications.models import UserNotificationOption, NotificationTemplate, UserNotification, UserNotificationSetting


class NotificationManager:
    def __init__(self, user):
        self.user = user

    def create_notification(self, notification_template_id, *args):
        try:
            template = NotificationTemplate.objects.get(id=notification_template_id)

            # Determine notification type
            user_settings = UserNotificationSetting.objects.filter(user=self.user).first()
            notification_type = 0
            if user_settings:
                if user_settings.push_notification:
                    notification_type = 1

            notification = UserNotification.objects.create(
                user=self.user,
                notification_template=template,
                notification_type=notification_type,
                status=0
            )

            options = [
                UserNotificationOption(
                    user_notification=notification,
                    field_id=index,
                    txt=value
                ) for index, value in enumerate(args)
            ]
            UserNotificationOption.objects.bulk_create(options)

            return notification
        except NotificationTemplate.DoesNotExist:
            raise ValueError("Notification template not found")
        except Exception as e:
            raise RuntimeError(f"Error creating notification: {str(e)}")