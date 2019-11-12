from rest_framework import serializers, status

from .models import Question, Answer, UserAnswer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'text')
        read_only_fields = ('id', 'text')


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'answers', 'type')
        read_only_fields = ('id', 'text', 'answers', 'type')


class UserAnswersSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    answer_ids = serializers.ListField(
        child=serializers.IntegerField()
    )
    question_id = serializers.IntegerField()

    def is_valid(self, raise_exception=False):
        is_valid = super(UserAnswersSerializer, self).is_valid(raise_exception)
        if is_valid:
            answer_ids = self.initial_data['answer_ids']
            question_id = self.initial_data['question_id']
            answers = Answer.objects.filter(id__in=answer_ids, question_id=question_id)
            if answers.count() != len(answer_ids):
                if raise_exception:
                    raise serializers.ValidationError('Invalid answers ids')
                return False
        return is_valid

    def create(self, validated_data):
        answer_ids = validated_data.get('answer_ids', [])
        return [UserAnswer.objects.create(user=self.context['request'].user, answer_id=answer_id) for answer_id in
                answer_ids]
