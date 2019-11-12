from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import permissions, status, mixins
from rest_framework.viewsets import GenericViewSet

from .models import Answer, Question
from .serializers import QuestionSerializer, UserAnswersSerializer


class QuestionViewSet(mixins.ListModelMixin, GenericViewSet):
    http_method_names = ['get', 'post']
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Question.objects.all()

    def get_queryset(self):
        return self.queryset.filter(
            is_active=True).exclude(
            answers__user_answers__user=self.request.user)

    @action(methods=['post', ], detail=True, serializer_class=UserAnswersSerializer,
            url_path='answer', permission_classes=[permissions.IsAuthenticated])
    def create_answer(self, request, **kwargs):
        obj = self.get_object()
        data = request.data.copy()
        data['question_id'] = kwargs['pk']
        context = {'request': self.request}
        serializer = self.serializer_class(data=data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(status=status.HTTP_201_CREATED)
