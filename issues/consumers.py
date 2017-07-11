import logging
import json

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http


from .models import CommunicationsIssue


@channel_session
def ws_notify_issue(message):
    logging.debug('websocket_connect. dict = %s', message)
    response_dcit = {'text': json.dumps({
            'username': message.user.username,
            'is_ready_accept_issues': True
        })}
    logging.debug('websocket_connect. dict = %s', response_dcit)
    Group('users').send(response_dcit)
