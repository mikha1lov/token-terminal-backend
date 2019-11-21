from datetime import datetime

from django.db.models import Q

from rest_framework import permissions, mixins, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Meeting, MeetingStatus
from .serializers import MeetingSerializer


class MeetingViewSet(mixins.ListModelMixin, GenericViewSet):
    http_method_names = ['get', 'post']
    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Meeting.objects.all()

    def get_queryset(self):
        return self.queryset.filter(
            users=self.request.user)

    def list(self, request, *args, **kwargs):
        data = {}
        now = datetime.now()
        user = request.user
        accepted_meetings = self.get_queryset().filter(statuses__user=user, statuses__status=MeetingStatus.ACCEPTED, datetime__gt=now)
        inactive_meetings = self.get_queryset().filter(Q(statuses__user=user, statuses__status=MeetingStatus.DECLINED)
                                                       | Q(statuses__user=user, datetime__lte=datetime.now().date())).distinct()
        new_meetings = self.get_queryset().filter(statuses__user=user, statuses__status=None, datetime__gt=now).distinct()
        data['accepted'] = MeetingSerializer(accepted_meetings, many=True, context={'request': request}).data
        data['inactive'] = MeetingSerializer(inactive_meetings, many=True, context={'request': request}).data
        data['new'] = MeetingSerializer(new_meetings, many=True, context={'request': request}).data
        return Response(data=data)

    @action(methods=['post', ], detail=True, serializer_class=serializers.Serializer,
            url_path='accept', permission_classes=[permissions.IsAuthenticated])
    def accept_meeting(self, request, **kwargs):
        self._update_meeting_status(MeetingStatus.ACCEPTED)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['post', ], detail=True, serializer_class=serializers.Serializer,
            url_path='decline', permission_classes=[permissions.IsAuthenticated])
    def decline_meeting(self, request, **kwargs):
        self._update_meeting_status(MeetingStatus.DECLINED)
        return Response(status=status.HTTP_200_OK)

    def _update_meeting_status(self, new_status):
        meeting = self.get_object()
        meeting_status = meeting.statuses.get(user=self.request.user)
        meeting_status.status = new_status
        meeting_status.save()
