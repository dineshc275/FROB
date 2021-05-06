import uuid

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone

from FROB.custom_storages import BookClubMediaStorage, EventUserMediaStorage, EventMediaStorage, \
    BookTalkMediaStorage
from account.models import UserAccount, UserHistory
from app_data.models import Banner
from book.models import Book
DEFAULT_CHOICE_1 = (("invited", "Invited"),
                    ("accepted", "Accepted"))


class CommonFields(models.Model):
    created_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    deleted_timestamp = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        abstract = True


class BookClub(CommonFields):
    id = models.CharField(primary_key=True, max_length=150, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255, blank=True, null=True)
    short_description = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    visit_count = models.PositiveIntegerField(default=1)
    manual_popularity = models.PositiveIntegerField(default=1)
    books = models.ManyToManyField(Book, through="BookClubBook")
    user_history = GenericRelation(UserHistory, related_name='book_club_user_history',)
    banner = GenericRelation(Banner, related_name='book_club_banner')

    class Meta:
        db_table = 'bookclub'
        managed = True


class BookClubMedia(CommonFields):
    id = models.CharField(primary_key=True, max_length=150, editable=False, default=uuid.uuid4)
    media = models.FileField(storage=BookClubMediaStorage())
    bookclub = models.ForeignKey(BookClub, null=True, blank=True, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = 'bookclub_media'
        managed = True


class BookClubFollower(CommonFields):
    id = models.CharField(primary_key=True, max_length=150, editable=False, default=uuid.uuid4)
    bookclub = models.ForeignKey(BookClub, null=True, blank=True, on_delete=models.CASCADE, related_name='bookclub_follower_bc')
    inviter = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="bcf_inviter", null=True, blank=True)
    receiver = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="bcf_receiver")
    receiver_status = models.CharField(max_length=50, choices=DEFAULT_CHOICE_1, default="accepted")
    accepted_timestamp = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'bookclub_follower'
        managed = True


class BookClubKeyContributor(CommonFields):
    id = models.CharField(primary_key=True, max_length=150, editable=False, default=uuid.uuid4)
    bookclub = models.ForeignKey(BookClub, null=True, blank=True, on_delete=models.CASCADE, related_name='bckc_bc')
    inviter = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="bckc_inviter")
    receiver = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="bckc_receiver")
    receiver_status = models.CharField(max_length=50, choices=DEFAULT_CHOICE_1, default="invited")
    accepted_timestamp = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'bookclub_key_contributor'
        managed = True


class BookClubKeyUser(CommonFields):
    id = models.CharField(primary_key=True, max_length=150, editable=False, default=uuid.uuid4)
    bookclub = models.ForeignKey(BookClub, null=True, blank=True, on_delete=models.CASCADE, related_name='bcku_bc')
    inviter = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="bcku_inviter")
    receiver = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="bcku_receiver")
    receiver_status = models.CharField(max_length=50, choices=DEFAULT_CHOICE_1, default="invited")
    accepted_timestamp = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'bookclub_key_user'
        managed = True


class Event(CommonFields):
    id = models.CharField(primary_key=True, max_length=150, editable=False, default=uuid.uuid4)
    bookclub = models.ForeignKey(BookClub, null=True, blank=True, on_delete=models.CASCADE, related_name='bookclub_event')
    name = models.CharField(max_length=250)
    short_description = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    from_timestamp = models.DateTimeField()
    to_timestamp = models.DateTimeField()
    link = models.CharField(max_length=250, null=True, blank=True)
    fee = models.PositiveIntegerField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    banner = GenericRelation(Banner, related_name='event_banner')

    class Meta:
        db_table = 'event'
        managed = True


class EventUser(CommonFields):
    id = models.CharField(primary_key=True, max_length=150, editable=False, default=uuid.uuid4)
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE, related_name='event_user_event')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="event_user_user")
    media = models.FileField(storage=EventUserMediaStorage(), null=True, blank=True)

    class Meta:
        db_table = 'event_user'
        managed = True


class EventMedia(CommonFields):
    id = models.CharField(primary_key=True, max_length=150, editable=False, default=uuid.uuid4)
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE, related_name='event_media')
    media = models.FileField(storage=EventMediaStorage(), null=True, blank=True)
    is_primary = models.BooleanField(default=False)
    link = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'event_media'
        managed = True


class EventSubscribe(CommonFields):
    id = models.CharField(primary_key=True, max_length=150, editable=False, default=uuid.uuid4)
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE, related_name='event_subscribe_event')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="event_subscribe_user")
    is_subscribed = models.BooleanField(default=True)
    is_attending = models.BooleanField(default=True)
    is_attended = models.BooleanField(default=False)

    class Meta:
        db_table = 'event_subscribe'
        managed = True


class BookClubBook(CommonFields):
    id = models.CharField(primary_key=True, max_length=150, editable=False, default=uuid.uuid4)
    bookclub = models.ForeignKey(BookClub, on_delete=models.CASCADE, related_name='bookclub_book_bc')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='bookclub_book_b')

    class Meta:
        db_table = 'bookclub_book'
        managed = True
