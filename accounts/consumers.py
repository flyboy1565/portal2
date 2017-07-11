import json
import logging
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http

logger = logging.getLogger(__name__)


@channel_session_user_from_http
def ws_connect(message):
    logger.info('websocket_connect. message = %s', message)
    Group('users').add(message.reply_channel)
    Group('users').send({
        'text': json.dumps({
            'username': message.user.username,
            'is_logged_in': True
        })
    })


@channel_session_user
def ws_disconnect(message):
    Group('users').send({
        'text': json.dumps({
            'username': message.user.username,
            'is_logged_in': False
        })
    })
    Group('users').discard(message.reply_channel)