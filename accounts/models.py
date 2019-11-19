from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from project.constants import PLACE_TYPE_CHOICE


class User(AbstractUser):
    avatar = models.ImageField(blank=True, null=True)


class Profile(models.Model):
    EVERY_WEEK = 'every_week'
    EVERY_MONTH = 'every_month'

    MEETING_FREQUENCY_CHOICE = (
        (EVERY_WEEK, 'Every week'),
        (EVERY_MONTH, 'Every month'),
    )

    user = models.OneToOneField(User, related_name='profile', on_delete=models.deletion.CASCADE)
    meeting_frequency = models.CharField(max_length=255, choices=MEETING_FREQUENCY_CHOICE, null=True, blank=True)
    meeting_type = models.CharField(max_length=255, choices=PLACE_TYPE_CHOICE, null=True, blank=True)
    is_active = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
