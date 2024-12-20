from rest_framework import serializers
from .models import UserNotificationOption, UserNotification, NotificationCategory, NotificationTemplate


class NotificationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationCategory
        fields = ['id', 'name', 'title']


class NotificationTemplateSerializer(serializers.ModelSerializer):
    notification_category = serializers.SerializerMethodField()

    class Meta:
        model = NotificationTemplate
        fields = ['id', 'name', 'txt', 'notification_category']



class UserNotificationOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotificationOption
        fields = ['field_id', 'txt']


class UserNotificationSerializer(serializers.ModelSerializer):
    formatted_txt = serializers.SerializerMethodField()

    class Meta:
        model = UserNotification
        fields = ['id', 'notification_type', 'status', 'created', 'formatted_txt']

    def get_formatted_txt(self, obj):
        template = obj.notification_template
        user_language_id = self.context['request'].user.language_id
        translated_text = template.txt

        if user_language_id != 1:
            if hasattr(template, 'prefetched_translations') and template.prefetched_translations:
                translated_text = template.prefetched_translations[0].text

        options = list(obj.options.order_by('field_id').values_list('txt', flat=True))

        try:
            return translated_text.format(*options)
        except (IndexError, KeyError) as e:
            return f"Error formatting notification: {str(e)}"