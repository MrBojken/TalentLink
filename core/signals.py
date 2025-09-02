from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from .models import Profile


@receiver(user_signed_up)
def create_profile_on_social_signup(sender, request, user, **kwargs):
    """
    Signal receiver to create a Profile for a new social account.
    """
    if not Profile.objects.filter(user=user).exists():
        Profile.objects.create(user=user)