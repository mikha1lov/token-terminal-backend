from rest_framework import serializers
from rest_framework.authtoken.models import Token

from accounts.models import User, Profile
from accounts.utils import signed_data, verify_address, verify_signature
from project.constants import PLACE_TYPE_CHOICE


class PublicUserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'avatar')


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()
    meeting_frequency = serializers.ChoiceField(source='profile.meeting_frequency',
                                                choices=Profile.MEETING_FREQUENCY_CHOICE)
    meeting_type = serializers.ChoiceField(source='profile.meeting_type',
                                           choices=PLACE_TYPE_CHOICE)
    is_active = serializers.BooleanField(source='profile.is_active')

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'username', 'avatar',
                  'meeting_frequency', 'meeting_type', 'is_active')
        read_only_fields = ('id', 'username')

    def update(self, instance, validated_data):
        try:
            profile = instance.profile
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance)
            profile = instance.profile

        profile_data = validated_data.pop('profile', {})
        for key, value in profile_data.items():
            setattr(profile, key, value)
        profile.save()
        return super(UserSerializer, self).update(instance, validated_data)


class SuccessAuthSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Token
        fields = ('key', 'created', 'user')


class WavesAuthSerializer(serializers.Serializer):
    address = serializers.CharField(required=True)
    pub_key = serializers.CharField(required=True)
    signature = serializers.CharField(required=True)
    host = serializers.CharField(required=True)
    data = serializers.CharField(required=True)

    def validate(self, attrs):
        address = attrs.get('address')
        pub_key = attrs.get('pub_key')
        signature = attrs.get('signature')
        host = attrs.get('host')
        data = attrs.get('data')
        message_bytes = signed_data(host, data)

        is_valid_signature = verify_signature(pub_key, signature, message_bytes)
        is_valid_address = verify_address(pub_key, address)

        if not is_valid_signature:
            raise serializers.ValidationError('Invalid signature', code='authorization')
        elif not is_valid_address:
            raise serializers.ValidationError('Invalid address', code='authorization')
        return attrs
