from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models

class UserRole(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "user_role"

class Language(models.Model):
    name = models.CharField(max_length=32, null=True, blank=True)
    title = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        db_table = 'language'

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