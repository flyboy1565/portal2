import logging

from django.contrib.auth import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from rest_framework.authtoken.models import Token

from accounts.models import LoggedInUser


@receiver(user_logged_in)
def on_user_login(sender, **kwargs):
    logging.debug('Login = %s', sender)
    LoggedInUser.objects.get_or_create(user=kwargs.get('user'))
    

@receiver(user_logged_out)
def on_user_logout(sender, **kwargs):
    logging.debug('Logout = %s', sender)
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
