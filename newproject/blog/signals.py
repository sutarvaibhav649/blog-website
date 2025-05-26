from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from . import models


@receiver(post_save,sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        models.UserProfile.objects.create(user = instance)