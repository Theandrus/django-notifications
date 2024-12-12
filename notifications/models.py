from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models



class Country(models.Model):
    name = models.CharField(max_length=25, null=True, blank=True)
    code = models.CharField(max_length=5, null=True, blank=True)
    code_exp = models.CharField(max_length=5, null=True, blank=True)

    class Meta:
        db_table = 'country'


class Language(models.Model):
    name = models.CharField(max_length=32, null=True, blank=True)
    title = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        db_table = 'language'


class NotificationCategory(models.Model):
    name = models.CharField(max_length=32, null=True, blank=True)
    title = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        db_table = 'notification_category'


class NotificationTemplate(models.Model):
    notification_category = models.ForeignKey(
        NotificationCategory, on_delete=models.CASCADE, related_name="templates"
    )
    name = models.CharField(max_length=32, null=True, blank=True)
    txt = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "notification_template"


class UserRole(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "user_role"


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    role = models.ForeignKey("UserRole", on_delete=models.SET_NULL, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=False)
    verified = models.BooleanField(null=True, blank=True)
    language = models.ForeignKey("Language", on_delete=models.CASCADE, default=1)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email


    class Meta:
        db_table = "user"


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
        NotificationTemplate, on_delete=models.CASCADE, null=True, blank=True
    )
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


class TranslationString(models.Model):
    content_type = models.ForeignKey(
        "contenttypes.ContentType", on_delete=models.CASCADE, null=True, blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    translation_field_id = models.PositiveSmallIntegerField(null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'translation_string'