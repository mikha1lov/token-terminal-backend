from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.viewsets import GenericViewSet

from accounts.models import User
from accounts.serializers import WavesAuthSerializer, SuccessAuthSerializer


class AuthViewSet(GenericViewSet):
    http_method_names = ['post', ]

    @action(methods=['post', ], detail=False, serializer_class=WavesAuthSerializer,
            url_path='auth', permission_classes=[permissions.AllowAny])
    def auth(self, request):
        """
        Generate data for auth in Waves Keeper
        """
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user, _ = User.objects.get_or_create(username=serializer.data['address'])
            token, _ = Token.objects.get_or_create(user=user)
            response = SuccessAuthSerializer(token)
            return Response(response.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
