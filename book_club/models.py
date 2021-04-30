import uuid

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from FROB.custom_storages import BookClubMediaStorage, EventUserMediaStorage, EventMediaStorage, \
    BookClubTalkMediaStorage
from account.models import UserAccount, UserHistory
from app_data.models import Banner
from book.models import Book


class BookClub(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255, blank=True, null=True)
    short_description = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    visit_count = models.PositiveIntegerField(default=1)
    manual_popularity = models.PositiveIntegerField(default=1)
    books = models.ManyToManyField(Book, through="BookClubBook")
    user_history = GenericRelation(UserHistory, related_name='book_club_user_history',)
    banner = GenericRelation(Banner, related_name='book_club_banner')

    created_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="bookclub_created_user")
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    deleted_timestamp = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'bookclub'
        managed = True


class BookClubMedia(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    media = models.FileField(storage=BookClubMediaStorage())
    bookclub = models.ForeignKey(BookClub, null=True, blank=True, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)

    created_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="bookclub_media_created_user")
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    deleted_timestamp = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'bookclub_media'
        managed = True


class BookClubUser(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    bookclub = models.ForeignKey(BookClub, null=True, blank=True, on_delete=models.CASCADE, related_name='bookclub_user')
    is_contributor = models.BooleanField(default=False)
    is_key_user = models.BooleanField(default=False)
    is_follower = models.BooleanField(default=True)

    created_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="bookclub_user_created_user")
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    deleted_timestamp = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'bookclub_user'
        managed = True


class Event(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    bookclub = models.ForeignKey(BookClub, null=True, blank=True, on_delete=models.CASCADE, related_name='bookclub_event')
    name = models.CharField(max_length=250)
    short_description = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    event_from = models.DateTimeField()
    event_to = models.DateTimeField()
    link = models.CharField(max_length=250, null=True, blank=True)
    fee = models.PositiveIntegerField(null=True, blank=True)
    banner = GenericRelation(Banner, related_name='event_banner')

    created_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="event_created_user")
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    deleted_timestamp = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'event'
        managed = True


class EventUser(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE, related_name='event_user_event')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="event_user_user")
    media = models.FileField(storage=EventUserMediaStorage(), null=True, blank=True)

    created_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="event_user_created_user")
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    deleted_timestamp = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'event_user'
        managed = True


class EventMedia(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE, related_name='event_media')
    media = models.FileField(storage=EventMediaStorage())
    is_primary = models.BooleanField(default=False)

    created_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="event_media_created_user")
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    deleted_timestamp = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'event_media'
        managed = True


class EventSubscribe(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE, related_name='event_subscribe_event')
    is_subscribed = models.BooleanField(default=True)
    is_attending = models.BooleanField(default=False)
    is_attended = models.BooleanField(default=False)

    created_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="event_subscribe_created_user")
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    deleted_timestamp = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'event_subscribe'
        managed = True


class BookClubTalk(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    bookclub = models.ForeignKey(BookClub, null=True, blank=True, on_delete=models.CASCADE, related_name='bookclub_talk')
    media = models.FileField(storage=BookClubTalkMediaStorage())
    talk_by = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="bookclub_talk_user", null=True, blank=True)
    talk_by_other = models.CharField(max_length=255, null=True, blank=True)
    is_audio = models.BooleanField(default=True)
    banner = GenericRelation(Banner, related_name='book_club_talk_banner')

    created_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="bookclub_talk_created_user")
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    deleted_timestamp = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'bookclub_talk'
        managed = True


class BookClubBook(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    bookclub = models.ForeignKey(BookClub, on_delete=models.CASCADE, related_name='bookclub_book_bc')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='bookclub_book_b')

    created_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="bookclub_book_created_user")
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    deleted_timestamp = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'bookclub_book'
        managed = True
