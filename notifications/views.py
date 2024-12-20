from django.contrib.contenttypes.models import ContentType
from django.db.models import Prefetch
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .filters import UserNotificationFilter
from .serializers import UserNotificationSerializer
from .models import UserNotification, NotificationTemplate, UserNotificationOption, TranslationString, \
    UserNotificationSetting
from .services import NotificationManager


class NotificationListView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserNotificationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserNotificationFilter

    def get_queryset(self):
        user_language_id = self.request.user.language_id
        content_type = ContentType.objects.get_for_model(NotificationTemplate)

        # Prefetch translations and options
        translations_prefetch = Prefetch(
            'notification_template__translations',
            queryset=TranslationString.objects.filter(
                content_type=content_type,
                language_id=user_language_id
            ),
            to_attr='prefetched_translations'
        )

        options_prefetch = Prefetch(
            'options',
            queryset=UserNotificationOption.objects.all()
        )

        # Fetch user notification settings and filter by type
        user_settings = UserNotificationSetting.objects.filter(user=self.request.user).first()
        notification_type_filter = []
        if user_settings:
            if user_settings.system_notification:
                notification_type_filter.append(0)
            if user_settings.push_notification:
                notification_type_filter.append(1)
        else:
            notification_type_filter = [0]  # Default to system notifications

        return UserNotification.objects.filter(
            user=self.request.user,
            notification_type__in=notification_type_filter
        ).prefetch_related(translations_prefetch, options_prefetch)


class CreateNotificationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        try:
            notification_template_id = data.get("notification_template_id")
            args = data.get("args", [])  # Ensure args is a list

            if not isinstance(args, list):
                return Response({"error": "Invalid 'args' format. Must be a list."}, status=400)

            # Fetch the template to validate
            manager = NotificationManager(user)
            notification = manager.create_notification(notification_template_id, *args)

            return Response(
                {"message": "Notification created successfully", "id": notification.id},
                status=201
            )
        except NotificationTemplate.DoesNotExist:
            return Response({"error": "Notification template not found."}, status=404)
        except ValueError as ve:
            return Response({"error": f"{str(ve)}"}, status=400)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=500)


class UpdateNotificationStatusView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, notification_id):
        try:
            notification = UserNotification.objects.get(id=notification_id, user=request.user)
            notification.status = 1
            notification.save()

            return Response({
                "message": "Notification status updated",
                "id": notification.id,
                "status": notification.status
            }, status=200)

        except UserNotification.DoesNotExist:
            return Response({"error": "Notification not found or does not belong to the user"}, status=404)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=500)



