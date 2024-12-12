from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .filters import NotificationFilter
from .serializers import UserNotificationSerializer
from .models import UserNotification, NotificationTemplate, UserNotificationOption


class NotificationManager:

    def __init__(self, user):
        self.user = user

    def create_notification(self, notification_template_id, project_id, project_name):
        try:
            template = NotificationTemplate.objects.get(id=notification_template_id)
            notification = UserNotification.objects.create(
                user=self.user,
                notification_template=template,
                notification_type=1,
                status=0,
            )

            UserNotificationOption.objects.bulk_create([
                UserNotificationOption(
                    user_notification=notification,
                    field_id=1,
                    txt=str(project_id)
                ),
                UserNotificationOption(
                    user_notification=notification,
                    field_id=2,
                    txt=project_name
                ),
            ])

            return notification

        except NotificationTemplate.DoesNotExist:
            raise ValueError("Notification template not found")
        except Exception as e:
            raise RuntimeError(f"Error creating notification: {str(e)}")


class NotificationListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        filters = {
            'status': request.query_params.get('status'),
            'notification_type': request.query_params.get('notification_type'),
            'notification_category': request.query_params.get('notification_category'),
        }

        notifications = NotificationFilter.filter_notifications(request.user, filters)
        serializer = UserNotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class CreateNotificationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        notification_template_id = data.get('notification_template_id')
        project_id = data.get('project_id')
        project_name = data.get('project_name')

        try:
            manager = NotificationManager(user)
            notification = manager.create_notification(
                notification_template_id=notification_template_id,
                project_id=project_id,
                project_name=project_name
            )

            return Response({"message": "Notification created", "id": notification.id}, status=201)

        except ValueError as e:
            return Response({"error": str(e)}, status=400)
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


