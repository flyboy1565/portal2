
import logging

from json import dumps

from django.db.models.signals import post_save, post_delete
from django.core.serializers import serialize
from django.dispatch import receiver

from channels import Group

from .models import CommunicationsIssue


logger = logging.getLogger(__name__).setLevel(logging.DEBUG)


def send_notification(notification):
    logging.debug('send_notification. notification = %s', notification)
    Group("issues").send({'text': dumps(notification)})


@receiver(post_save, sender=CommunicationsIssue)
def incident_post_save(sender, **kwargs):
    logging.debug('Sender = %s', sender)
    instance = serialize('json', [ kwargs['instance'], ])
    send_notification({
        'type': 'post_save',
        'created': kwargs['created'],
        'feature': instance,
    })