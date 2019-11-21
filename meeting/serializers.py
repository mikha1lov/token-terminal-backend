from rest_framework import serializers

from accounts.serializers import PublicUserSerializer
from meeting.models import Place, Meeting, MeetingStatus


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('name', 'address')


class MeetingStatusSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id')

    class Meta:
        model = MeetingStatus
        fields = ('user_id', 'status')


class MeetingSerializer(serializers.ModelSerializer):
    place = PlaceSerializer()
    users = PublicUserSerializer(many=True)
    statuses = MeetingStatusSerializer(many=True)

    class Meta:
        model = Meeting
        fields = ('id', 'datetime', 'place', 'users', 'statuses',)
