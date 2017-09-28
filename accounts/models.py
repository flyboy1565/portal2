from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class LoggedInUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='logged_in_user')
    uid = models.CharField(max_length=15, null=True, blank=True)
    created_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_via = models.CharField(max_length=10, choices=(('LDAP', 'LDAP'), ('Manually', 'Manually'), ('App', 'Application')))
    
    def __str__(self):
        return self.user.username
        

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    shsg = models.BooleanField(default=False)
    hsrg = models.BooleanField(default=False)
    wan = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()