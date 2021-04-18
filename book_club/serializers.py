from django.db.models import Q
from rest_framework import serializers
from book_club.models import BookClub, BookClubImage


class BookClubImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookClubImage
        fields = ('id', 'image')


class BookClubSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image')
    key_user = serializers.SerializerMethodField('get_key_user')

    class Meta:
        model = BookClub
        fields = ('id', "name", "key_user", "short_description", "description", "image", "ip")

    def get_image(self, ob):
        image_obj = BookClubImage.objects.filter(Q(book_club=ob.id) & Q(is_deleted=False) & Q(is_active=True))
        serializer = BookClubImageSerializer(image_obj, many=True)
        return serializer.data

    def get_key_user(self, ob):
        if ob.key_user:
            return ob.key_user.first_name
        else:
            return None
