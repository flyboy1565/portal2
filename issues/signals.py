
import logging

from json import dumps

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from channels import Group

from .models import CommunicationsIssue, WorkOn
from .api.serializers import IssueSerializer


logger = logging.getLogger(__name__).setLevel(logging.DEBUG)


def send_notification(notification):
    logging.debug('send_notification. notification = %s', notification)
    print(notification)
    Group("users").send({'text': dumps(notification)})


@receiver(post_save, sender=CommunicationsIssue)
def incident_post_save(sender, **kwargs):
    logging.debug('Sender = %s', sender)
    obj = CommunicationsIssue.objects.get(pk=kwargs['instance'].pk)
    instance = IssueSerializer(obj).data  # <<<< this
    send_notification({
        'type': 'post_save',
        'created': kwargs['created'],
        'resolved': obj.resolved,
        'feature': instance,
    })
    