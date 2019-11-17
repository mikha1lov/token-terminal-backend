from rest_framework import permissions, mixins
from rest_framework.viewsets import GenericViewSet

from .models import Meeting, MeetingStatus
from .serializers import MeetingSerializer


class MeetingViewSet(mixins.ListModelMixin, GenericViewSet):
    http_method_names = ['get', ]
    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Meeting.objects.all()

    def get_queryset(self):
        return self.queryset.filter(
            users=self.request.user).exclude(
            statuses__status=MeetingStatus.DECLINED
        )
