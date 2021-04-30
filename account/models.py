import datetime
import uuid
import jwt
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken

from FROB.constant_values import otp_validity_minutes

OTP_TYPE_CHOICES = (("register", "Register"),
                    ("login", "Login"),
                    ("forgot_password", "Forgot Password"))


class UserManager(BaseUserManager):
    def create_user(self, mobile, first_name=None, email=None, password=None):
        if mobile is None:
            raise TypeError('User must have a Mobile')
        user = self.model(first_name=first_name, email=self.normalize_email(email), mobile=mobile)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

    def create_mobile_user(self, mobile, msg91_id=None):
        user = self.model(mobile=mobile)
        # user.otp_id = msg91_id
        user.is_active = True
        user.is_mobile_verified = True
        user.save()
        return user

    def create_social_user(self, user_id, first_name, email=None):
        user = self.model(user_id=user_id, first_name=first_name, email=email)
        user.is_active = True
        user.save()
        return user

    def create_superuser(self, password, mobile, first_name=None, user_id=None):
        user = self.model(first_name=first_name, mobile=mobile, user_id=user_id)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(primary_key=True, editable=True, default=uuid.uuid4, unique=True, max_length=500, name="id")
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True)
    is_mobile_verified = models.BooleanField(default=False)
    email = models.EmailField(blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    signup_timestamp = models.DateTimeField(auto_now_add=True)
    secret_key = models.UUIDField(default=uuid.uuid4, editable=False)

    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    deleted_timestamp = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    ip = models.GenericIPAddressField(null=True, blank=True)

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return "{}".format(self.id)

    def __user_id__(self):
        return self.id

    class Meta:
        db_table = 'user_account'
        managed = True

    @staticmethod
    def generate_token(user):
        refresh = RefreshToken.for_user(user)
        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return token


class BlockedToken(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=500)
    user = models.ForeignKey(UserAccount, related_name="token_user", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("token", "user")
        db_table = 'blocked_token'
        managed = True


class LoginTrack(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserAccount, related_name="login_track_user", on_delete=models.CASCADE)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    deleted_timestamp = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = "login_track"
        managed = True


class Otp(models.Model):
    id = models.AutoField(primary_key=True)
    input = models.TextField(blank=True, null=True)
    request_id = models.TextField(blank=True, null=True)
    otp_type = models.CharField(choices=OTP_TYPE_CHOICES, default="register", max_length=50)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    expiry_timestamp = models.DateTimeField(
        default=datetime.datetime.now() + datetime.timedelta(minutes=otp_validity_minutes))
    otp = models.IntegerField(blank=True, null=True)
    attempts = models.PositiveIntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'otp'


class UserHistory(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=False)
    content_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'content_id')
    user = models.ForeignKey(UserAccount, related_name="user_history_user", on_delete=models.CASCADE)

    created_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="user_history_created_user")
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    deleted_timestamp = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'user_history'
        managed = True
