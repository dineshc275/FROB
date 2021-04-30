from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
import uuid
# Create your models here.
from FROB.custom_storages import BookMediaStorage
from account.models import UserAccount, UserHistory
from app_data.models import Banner

BOOK_CHOICE_SOURCE = (("amazon", "Amazon"),
                      ("flipkart", "Flipkart"))


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    visit_count = models.PositiveIntegerField(default=1)
    manual_popularity = models.PositiveIntegerField(default=1)
    user_history = GenericRelation(UserHistory, related_name='genre_user_history',)
    banner = GenericRelation(Banner, related_name='genre_banner')

    created_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="genre_created_user")
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    deleted_timestamp = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'genre'
        managed = True


class Book(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
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
    user_history = GenericRelation(UserHistory, related_name='book_user_history',)
    banner = GenericRelation(Banner, related_name='book_banner')

    created_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="book_created_user")
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    deleted_timestamp = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'book'
        managed = True


class BookPurchaseLink(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_purchase_link')
    source = models.CharField(max_length=120, null=True, blank=True, choices=BOOK_CHOICE_SOURCE)
    link = models.TextField()
    created_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE,
                                     related_name="book_purchase_link_created_user")

    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    deleted_timestamp = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'book_purchase_link'
        managed = True


class BookMedia(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    book = models.ForeignKey(Book, null=True, blank=True, on_delete=models.CASCADE, related_name='book_media')
    media = models.FileField(storage=BookMediaStorage())
    is_primary = models.BooleanField(default=False)

    created_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="book_media_created_user")
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    deleted_timestamp = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'book_media'
        managed = True


class BookGenre(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='bookgenre_genre')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='bookgenre_book')

    created_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="bookgenre_created_user")
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    deleted_timestamp = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'book_genre'
        managed = True
