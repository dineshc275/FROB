import uuid
from django.db import models

from FROB.custom_storages import BookClubMediaStorage
from account.models import UserAccount


class BookClub(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255, blank=True, null=True)
    key_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True, blank=True, related_name='book_club_key_user')
    short_description = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    created_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="book_club_created_user")
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    deleted_timestamp = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'book_club'
        managed = True


class BookClubImage(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    image = models.FileField(storage=BookClubMediaStorage())
    book_club = models.ForeignKey(BookClub, null=True, blank=True, on_delete=models.CASCADE)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    deleted_timestamp = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'bookclub_image'
        managed = True


class BookClubEvent(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    book_club = models.ForeignKey(BookClub, null=True, blank=True, on_delete=models.CASCADE, related_name='book_club_event')
    name = models.CharField(max_length=250)
    short_description = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    event_from = models.DateTimeField()
    event_to = models.DateTimeField()
    link = models.CharField(max_length=250, null=True, blank=True)
    fee = models.PositiveIntegerField(null=True, blank=True)

    created_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="book_club_event_created_user")
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    deleted_timestamp = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'bookclub_event'
        managed = True