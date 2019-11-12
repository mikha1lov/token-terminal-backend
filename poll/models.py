from django.db import models

from project.models import BaseModel

RADIO = 'radio'
CHECKBOX = 'checkbox'

QUESTION_TYPES = (
    (RADIO, 'radio'),
    (CHECKBOX, 'checkbox'),
)


class Question(BaseModel):
    text = models.TextField()
    type = models.CharField(max_length=255, choices=QUESTION_TYPES)
    is_active = models.BooleanField(default=True)


class Answer(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.deletion.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)


class UserAnswer(BaseModel):
    answer = models.ForeignKey(Answer, on_delete=models.deletion.CASCADE, related_name='user_answers')
    user = models.ForeignKey('accounts.User', on_delete=models.deletion.CASCADE, related_name='answers')
