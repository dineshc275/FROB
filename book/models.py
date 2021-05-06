from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
import uuid
# Create your models here.
from django.utils import timezone

from FROB.custom_storages import BookMediaStorage, BookTalkMediaStorage
from account.models import UserAccount, UserHistory
from app_data.models import Banner

BOOK_CHOICE_SOURCE = (("amazon", "Amazon"),
                      ("flipkart", "Flipkart"))

READ_ALONG_STATUS = (("pending", "Pending"),
                     ("accepted", "Accepted"),
                     ("rejected", "Rejected"))

BOOK_READ_STATUS = (("favourite", "Favourite"),
                    ("reading", "Reading"),
                    ("completed", "Completed"))


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


class Genre(CommonFields):
    id = models.CharField(primary_key=True, max_length=150, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    visit_count = models.PositiveIntegerField(default=1)
    manual_popularity = models.PositiveIntegerField(default=1)
    user_history = GenericRelation(UserHistory, related_name='genre_user_history', )
    banner = GenericRelation(Banner, related_name='genre_banner')

    class Meta:
        db_table = 'genre'
        managed = True


class Book(CommonFields):
    id = models.CharField(primary_key=True, max_length=150, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=250, null=True, blank=True)
    published_year = models.PositiveIntegerField(null=True, blank=True)
    publisher = models.CharField(max_length=250, null=True, blank=True)
    chapter_count = models.PositiveIntegerField(null=True, blank=True)
    pages_count = models.PositiveIntegerField(null=True, blank=True)
    visit_count = models.PositiveIntegerField(default=1)
    manual_popularity = models.PositiveIntegerField(default=1)
    genre = models.ManyToManyField(Genre, through="BookGenre")
    user_history = GenericRelation(UserHistory, related_name='book_user_history', )
    banner = GenericRelation(Banner, related_name='book_banner')

    class Meta:
        db_table = 'book'
        managed = True


class BookPurchaseLink(CommonFields):
    id = models.CharField(primary_key=True, max_length=150, editable=False, default=uuid.uuid4)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_purchase_link')
    source = models.CharField(max_length=120, null=True, blank=True, choices=BOOK_CHOICE_SOURCE)
    link = models.TextField()
    created_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE,
                                     related_name="book_purchase_link_created_user")

    class Meta:
        db_table = 'book_purchase_link'
        managed = True


class BookMedia(CommonFields):
    id = models.CharField(primary_key=True, max_length=150, editable=False, default=uuid.uuid4)
    book = models.ForeignKey(Book, null=True, blank=True, on_delete=models.CASCADE, related_name='book_media')
    media = models.FileField(storage=BookMediaStorage())
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = 'book_media'
        managed = True


class BookGenre(CommonFields):
    id = models.CharField(primary_key=True, max_length=150, editable=False, default=uuid.uuid4)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='bookgenre_genre')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='bookgenre_book')

    class Meta:
        db_table = 'book_genre'
        managed = True


class ReadAlong(CommonFields):
    id = models.CharField(primary_key=True, max_length=150, editable=False, default=uuid.uuid4)
    inviter = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="readalong_inviter")
    receiver = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="readalong_receiver")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='readalong_book')
    receiver_status = models.CharField(max_length=50, choices=READ_ALONG_STATUS, default="pending")
    accepted_timestamp = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'read_along'
        managed = True


class BookRead(CommonFields):
    id = models.CharField(primary_key=True, max_length=150, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="bookread_user")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='bookread_book')
    book_status = models.CharField(max_length=50, choices=BOOK_READ_STATUS, default="reading")
    completed_timestamp = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'book_read'
        managed = True


class BookTalk(CommonFields):
    id = models.CharField(primary_key=True, max_length=150, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    book = models.ForeignKey(Book, null=True, blank=True, on_delete=models.CASCADE, related_name='book_talk')
    media = models.FileField(storage=BookTalkMediaStorage())
    image = models.FileField(storage=BookTalkMediaStorage(), null=True, blank=True)
    talk_by = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="book_talk_user", null=True, blank=True)
    talk_by_other = models.CharField(max_length=255, null=True, blank=True)
    is_audio = models.BooleanField(default=True)
    banner = GenericRelation(Banner, related_name='book_talk_banner')

    class Meta:
        db_table = 'book_talk'
        managed = True


class BookTalkComment(CommonFields):
    id = models.CharField(primary_key=True, max_length=150, editable=False, default=uuid.uuid4)
    book_talk = models.ForeignKey(BookTalk, null=True, blank=True, on_delete=models.CASCADE, related_name='book_talk')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="book_talk_comment_user", null=True, blank=True)
    comment = models.TextField()

    class Meta:
        db_table = 'book_talk_comment'
        # unique_together=("book_talk", "user")
        managed = True
