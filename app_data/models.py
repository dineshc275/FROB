from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
import uuid
from FROB.custom_storages import BannerMediaStorage
from account.models import UserAccount


class Banner(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=False)
    content_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'content_id')
    media = models.FileField(storage=BannerMediaStorage())
    link = models.TextField(null=True, blank=True)

    created_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="banner_created_user")
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    deleted_timestamp = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'banner'
        managed = True
