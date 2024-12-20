from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from authorization.models import User, Language


class Country(models.Model):
    name = models.CharField(max_length=25, null=True, blank=True)
    code = models.CharField(max_length=5, null=True, blank=True)
    code_exp = models.CharField(max_length=5, null=True, blank=True)

    class Meta:
        db_table = 'country'


class NotificationCategory(models.Model):
    name = models.CharField(max_length=32, null=True, blank=True)
    title = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        db_table = 'notification_category'

class TranslationString(models.Model):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_item = GenericForeignKey('content_type', 'object_id')
    translation_field_id = models.PositiveSmallIntegerField(null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    text = models.TextField(max_length=255)

    class Meta:
        unique_together = (("content_type", "object_id", "language"),)
        db_table = 'translation_string'

    def __str__(self):
        return f"{self.content_type} | {self.object_id} | {self.language}"


class NotificationTemplate(models.Model):
    notification_category = models.ForeignKey(
        NotificationCategory, on_delete=models.CASCADE, related_name="templates"
    )
    name = models.CharField(max_length=32, null=True, blank=True)
    txt = models.TextField(null=True, blank=True)
    translations = GenericRelation(TranslationString, related_query_name='translations')

    class Meta:
        db_table = "notification_template"



class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=510, null=True, blank=True)
    address = models.CharField(max_length=510, null=True, blank=True)
    started = models.DateTimeField(auto_now_add=True)
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)

    class Meta:
        db_table = "project"


class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    notification_template = models.ForeignKey(
        NotificationTemplate, on_delete=models.CASCADE)
    notification_type = models.PositiveSmallIntegerField(default=1)
    status = models.PositiveSmallIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_notification'


class UserNotificationOption(models.Model):
    user_notification = models.ForeignKey(
        UserNotification, on_delete=models.CASCADE, related_name="options"
    )
    field_id = models.PositiveSmallIntegerField(null=True, blank=True)
    txt = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        db_table = 'user_notification_option'


class UserNotificationSetting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_settings")
    notification_template = models.ForeignKey(
        'notifications.NotificationTemplate', on_delete=models.CASCADE, null=True, blank=True
    )
    system_notification = models.BooleanField(default=True)
    push_notification = models.BooleanField(default=True)

    class Meta:
        db_table = 'user_notification_setting'


