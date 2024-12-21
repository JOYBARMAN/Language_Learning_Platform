from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import User, UserOtp, Profile


@receiver(post_save, sender=User)
def create_user_otp(sender, instance, created, **kwargs):
    if created:
        UserOtp.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
