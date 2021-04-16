from rest_framework import serializers

from account.models import UserAccount


class UserAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAccount
        fields = ('first_name', 'last_name', 'email', 'mobile')