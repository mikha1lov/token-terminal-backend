from rest_framework import serializers

from accounts.serializers import PublicUserSerializer
from meeting.models import Place, Meeting


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('name', 'address')


class MeetingSerializer(serializers.ModelSerializer):
    place = PlaceSerializer()
    users = PublicUserSerializer(many=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Meeting
        fields = ('id', 'datetime', 'place', 'users', 'status')
        read_only_fields = ['status', ]

    def get_status(self, obj):
        return obj.statuses.get(user=self.context['request'].user).status
