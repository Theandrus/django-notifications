from django.urls import path
from .views import NotificationListView, CreateNotificationView,  UpdateNotificationStatusView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('create/', CreateNotificationView.as_view(), name='create-notification'),
    path('<int:notification_id>/read/', UpdateNotificationStatusView.as_view(), name='update-notification-status'),
]