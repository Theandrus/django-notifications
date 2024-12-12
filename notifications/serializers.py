from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, UserNotificationOption, UserNotification, NotificationCategory, NotificationTemplate


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid email or password")

        if not user.check_password(password):
            raise AuthenticationFailed("Invalid email or password")

        if not user.active:
            raise AuthenticationFailed("User account is not active")

        tokens = RefreshToken.for_user(user)

        return {
            "access": str(tokens.access_token),
            "refresh": str(tokens),
        }

class NotificationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationCategory
        fields = ['id', 'name', 'title']


class NotificationTemplateSerializer(serializers.ModelSerializer):
    notification_category = serializers.SerializerMethodField()

    class Meta:
        model = NotificationTemplate
        fields = ['id', 'name', 'txt', 'notification_category']  # Add notification_category

    def get_notification_category(self, obj):
        if obj.notification_category:
            return {
                "id": obj.notification_category.id,
                "name": obj.notification_category.name,
                "title": obj.notification_category.title,
            }
        return None


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
        template_txt = obj.notification_template.txt
        options = UserNotificationOption.objects.filter(user_notification=obj)

        replacements = {}
        for option in options:
            if option.field_id == 1:
                replacements["project_id"] = option.txt
            elif option.field_id == 2:
                replacements["project_name"] = option.txt
        try:
            formatted_txt = template_txt.format(**replacements)
        except KeyError as e:
            formatted_txt = f"Error formatting notification: missing {str(e)}"

        return formatted_txt