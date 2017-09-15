from django.db import models
from django.conf import settings
# Create your models here.


class LoggedInUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='logged_in_user')
    uid = models.CharField(max_length=15, null=True, blank=True)
    created_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_via = models.CharField(max_length=10, choices=(('LDAP', 'LDAP'), ('Manually', 'Manually'), ('App', 'Application')))
    
    def __str__(self):
        return '{}'.format(self.user)