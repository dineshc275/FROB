from django.db.models import Q
from rest_framework import serializers
from book_club.models import BookClub, BookClubMedia


class BookClubMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookClubMedia
        fields = ('id', 'image')


class BookClubSerializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField('get_media')
    key_user = serializers.SerializerMethodField('get_key_user')

    class Meta:
        model = BookClub
        fields = ('id', "name", "key_user", "short_description", "description", "image", "ip")

    def get_media(self, ob):
        image_obj = BookClubMedia.objects.filter(Q(book_club=ob.id) & Q(is_deleted=False) & Q(is_active=True))
        serializer = BookClubMediaSerializer(image_obj, many=True)
        return serializer.data

    def get_key_user(self, ob):
        if ob.key_user:
            return ob.key_user.first_name
        else:
            return None
