from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import permissions, status, mixins
from rest_framework.viewsets import GenericViewSet

from accounts.models import User
from accounts.serializers import WavesAuthSerializer, SuccessAuthSerializer, UserSerializer


class UserViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    http_method_names = ['post', 'get', 'patch']
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = User.objects.all()

    def check_object_permissions(self, request, obj):
        super(UserViewSet, self).check_object_permissions(request, obj)
        if obj != self.request.user:
            raise PermissionDenied

    @action(methods=['get', ], detail=False, serializer_class=UserSerializer,
            url_path='info', permission_classes=[permissions.IsAuthenticated])
    def info(self, request):
        """
        User info
        """
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data)

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

    @action(methods=['get', ], detail=False, url_path='logout')
    def logout(self, request):
        """
        Delete current user auth token
        """
        auth_token = getattr(request._user, 'auth_token', None)
        if auth_token:
            auth_token.delete()
        return Response(status=status.HTTP_200_OK)
