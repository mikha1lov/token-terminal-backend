from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from project.constants import PLACE_TYPE_CHOICE
from project.models import BaseModel


class Place(BaseModel):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=PLACE_TYPE_CHOICE)

    def __str__(self):
        return self.name


class Meeting(BaseModel):
    datetime = models.DateTimeField()
    users = models.ManyToManyField('accounts.User')
    place = models.ForeignKey(Place, on_delete=models.deletion.CASCADE)

    def __str__(self):
        return f"Встреча в {self.place.name}"


class MeetingStatus(BaseModel):
    ACCEPTED = 'accepted'
    DECLINED = 'declined'

    STATUS_CHOICE = (
        (ACCEPTED, 'Accepted'),
        (DECLINED, 'Declined'),
    )

    user = models.ForeignKey('accounts.User', on_delete=models.deletion.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.deletion.CASCADE, related_name='statuses')
    status = models.CharField(max_length=255, choices=STATUS_CHOICE, null=True, blank=True)


@receiver(m2m_changed, sender=Meeting.users.through)
def create_meeting_status(sender, instance, action, **kwargs):
    if action == 'post_add':
        for user in instance.users.all():
            MeetingStatus.objects.get_or_create(meeting=instance, user=user)
