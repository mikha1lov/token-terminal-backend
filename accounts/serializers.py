from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from accounts.utils import signed_data, verify_signature, verify_address


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'username')
        read_only_fields = ('id', 'username')


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
