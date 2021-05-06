from django.db.models import Q
from rest_framework import serializers

from FROB.constant_values import default_query_1
from account.models import UserAccount
from app_data.models import Banner
from book.models import BookMedia, BookRead, BookTalk, Book, BookTalkComment
from book_club.models import BookClubMedia, BookClub, Event, BookClubKeyContributor, EventMedia, EventSubscribe


class UserAccountV1Serializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField('get_media')

    class Meta:
        model = UserAccount
        fields = ("id", "first_name", "media")

    def get_media(self, obj):
        if obj.media:
            return obj.media.url
        else:
            return None


class UserAccountTest2V1Serializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField('get_media')

    class Meta:
        model = UserAccount
        fields = ("id", "first_name", "media", "mobile", "email", "password")

    def get_media(self, obj):
        if obj.media:
            return obj.media.url
        else:
            return None


class HomepagePart1BannerV1Serializer(serializers.ModelSerializer):
    is_link = serializers.SerializerMethodField('get_is_link')
    media = serializers.SerializerMethodField('get_media')

    class Meta:
        model = Banner
        fields = ("id", "media", "link", "is_link")

    def get_is_link(self, obj):
        return True if obj.link else False

    def get_media(self, obj):
        if obj.media:
            return obj.media.url
        else:
            return None


class HomepagePart1BookReadV1Serializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField('get_media')
    name = serializers.SerializerMethodField('get_name')
    id = serializers.SerializerMethodField('get_id')

    class Meta:
        model = BookRead
        fields = ("id", "book_status", "media", "name")

    def get_media(self, obj):
        media_obj = BookMedia.objects.filter(default_query_1 & Q(book=obj.book.id) & Q(is_primary=True))
        return media_obj[0].media.url if media_obj else None

    def get_name(self, obj):
        return obj.book.name

    def get_id(self, obj):
        return obj.book.id


class HomepagePart1BookV1Serializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField('get_media')
    book_status = serializers.SerializerMethodField('get_book_status')

    class Meta:
        model = Book
        fields = ("id", "book_status", "media", "name")

    def get_media(self, obj):
        media_obj = BookMedia.objects.filter(default_query_1 & Q(book=obj.id) & Q(is_primary=True))
        return media_obj[0].media.url if media_obj else None

    def get_book_status(self, obj):
        return "random"


class HomepagePart1BookClubV1Serializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField('get_media')

    class Meta:
        model = BookClub
        fields = ("id", "name", "short_description", "media", "name")

    def get_media(self, obj):
        media_obj = BookClubMedia.objects.filter(default_query_1 & Q(bookclub=obj.id) & Q(is_primary=True))
        return media_obj[0].media.url if media_obj else None


class HomepagePart1BookTalkV1Serializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')
    talk_user = serializers.SerializerMethodField('get_talk_user')
    media = serializers.SerializerMethodField('get_media')

    class Meta:
        model = BookTalk
        fields = ("id", "name", "short_description", "media", "name", "talk_user")

    def get_name(self, obj):
        return obj.book.name

    def get_talk_user(self, obj):
        if obj.talk_by:
            return {"talk_by":obj.talk_by.first_name, "user_id": obj.talk_by.id, "is_user_present": True}
        else:
            return {"talk_by":obj.talk_by_other, "user_id": None, "is_user_present": False}

    def get_media(self, obj):
        if obj.media:
            return obj.media.url
        else:
            return None


class HomepagePart1EventV1Serializer(serializers.ModelSerializer):
    bookclub_name = serializers.SerializerMethodField('get_bookclub_name')

    class Meta:
        model = Event
        fields = ("id", "name", "short_description", "from_timestamp", "bookclub_name")

    def get_bookclub_name(self, obj):
        return obj.bookclub.name


class BookClubMediaV1Serializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField('get_media')

    class Meta:
        model = Event
        fields = ("id", "media", "is_primary")

    def get_media(self, obj):
        if obj.media:
            return obj.media.url
        else:
            return None


class BookClubEventV1Serializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ("id", "name", "description", "short_description", "from_timestamp", "to_timestamp", "link", "fee",
                  "location")


class BookTalkV1Serializer(serializers.ModelSerializer):
    talk_user = serializers.SerializerMethodField('get_talk_user')
    media = serializers.SerializerMethodField('get_media')
    image = serializers.SerializerMethodField('get_image')

    class Meta:
        model = BookTalk
        fields = ("id", "name", "description", "media", "image", "talk_user")

    def get_talk_user(self, obj):
        if obj.talk_by:
            return {"talk_by":obj.talk_by.first_name, "user_id": obj.talk_by.id, "is_user_present": True}
        else:
            return {"talk_by":obj.talk_by_other, "user_id": None, "is_user_present": False}

    def get_media(self, obj):
        if obj.media:
            return obj.media.url
        else:
            return None

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        else:
            return None


class BookV1Serializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField('get_media')

    class Meta:
        model = Book
        fields = ("id", "media", "name")

    def get_media(self, obj):
        media_obj = BookMedia.objects.filter(default_query_1 & Q(book=obj.id) & Q(is_primary=True))
        return media_obj[0].media.url if media_obj else None


class BookClubAPIV1Serializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField('get_media')
    key_contributors = serializers.SerializerMethodField('get_key_contributors')
    events = serializers.SerializerMethodField('get_events')
    talks = serializers.SerializerMethodField('get_talks')
    books = serializers.SerializerMethodField('get_books')

    class Meta:
        model = BookClub
        fields = ("id", "name", "description", "media", "key_contributors", "events", "talks", "books")

    def get_media(self, obj):
        media_obj = BookClubMedia.objects.filter(default_query_1 & Q(bookclub=obj.id))
        return BookClubMediaV1Serializer(media_obj, many=True).data

    def get_key_contributors(self, obj):
        key_contributor_obj = BookClubKeyContributor.objects.filter(default_query_1 & Q(bookclub=obj.id) &
                                                Q(receiver_status="accepted")).select_related("receiver")
        return UserAccountV1Serializer(key_contributor_obj, many=True).data

    def get_events(self, obj):
        event_obj = Event.objects.filter(default_query_1 & Q(bookclub=obj.id))
        return BookClubEventV1Serializer(event_obj, many=True).data

    def get_talks(self, obj):
        book_list = obj.values_list("books__book", flat=True)
        talk_obj = BookTalk.objects.filter(default_query_1 & Q(book__in=book_list))
        return BookTalkV1Serializer(talk_obj, many=True).data

    def get_books(self, obj):
        book_list = obj.values_list("books__book", flat=True)
        book_obj = Book.objects.filter(default_query_1 & Q(id__in=book_list))
        return BookV1Serializer(book_obj, many=True).data


class UserBookTalkV1Serializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField('get_media')

    class Meta:
        model = BookTalk
        fields = ("id", "name", "description", "media", "image")

    def get_media(self, obj):
        if obj.media:
            return obj.media.url
        else:
            return None


class BookMediaV1Serializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField('get_media')

    class Meta:
        model = BookMedia
        fields = ("id", "media", "is_primary")

    def get_media(self, obj):
        if obj.media:
            return obj.media.url
        else:
            return None


class BookTalkCommentV1Serializer(serializers.ModelSerializer):
    user = UserAccountV1Serializer()

    class Meta:
        model = BookTalkComment
        fields = ("id", "comment", "user")


class BookDetailV1Serializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField('get_media')
    genre = serializers.SerializerMethodField('get_genre')

    class Meta:
        model = Book
        fields = ("id", "media", "name", "description", "author", "published_year", "publisher", "chapter_count",
                  "pages_count", "")

    def get_media(self, obj):
        media_obj = BookMedia.objects.filter(default_query_1 & Q(book=obj.id))
        return BookMediaV1Serializer(media_obj, many=True).data

    def get_genre(self, obj):
        genre_obj = obj.genre.filter(book=obj.id)
        response = []
        for i in genre_obj:
            response.append({"id": i.id}) # add genre name here


class BookTalkDetailV1Serializer(serializers.ModelSerializer):
    talk_user = serializers.SerializerMethodField('get_talk_user')
    comment = serializers.SerializerMethodField('get_comment')
    image = serializers.SerializerMethodField('get_image')

    class Meta:
        model = BookTalk
        fields = ("id", "media", "name", "image", "description", "talk_user", "comment")

    def get_talk_user(self, obj):
        if obj.talk_by:
            return {"talk_by": obj.talk_by.first_name, "user_id": obj.talk_by.id, "is_user_present": True}
        else:
            return {"talk_by": obj.talk_by_other, "user_id": None, "is_user_present": False}

    def get_comment(self, obj):
        book_talk_comment_obj = BookTalkComment.objects.filter(default_query_1 & Q(book_talk=obj.id))
        return UserAccountV1Serializer(book_talk_comment_obj, many=True).data

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        else:
            return None


class EventMediaV1Serializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField('get_media')

    class Meta:
        model = EventMedia
        fields = ("id", "media", "is_primary", "link")

    def get_media(self, obj):
        if obj.media:
            return obj.media.url
        else:
            return None


class EventDetailV1Serializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField('get_media')

    class Meta:
        model = Event
        fields = ("id", "name", "short_description", "description", "from_timestamp", "to_timestamp", "link", "fee",
                  "location")

    def get_media(self, obj):
        event_media_obj = EventMedia.objects.filter(default_query_1 & Q(event=obj.id))
        return EventMediaV1Serializer(event_media_obj, many=True).data


class EventSubscribeV1Serializer(serializers.ModelSerializer):
    user = UserAccountV1Serializer()

    class Meta:
        model = EventSubscribe
        fields = ("id", "is_subscribed", "is_attending", "user")