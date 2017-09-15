import numbers
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

from locations.models import Store
from circuits.models import Circuit

from .choices import issues_choices


class CommunicationsIssue(models.Model):
    store = models.ForeignKey(Store)
    issue = models.CharField(max_length=5, choices=issues_choices())
    ticket = models.CharField(max_length=100, null=True, blank=True)
    down_since = models.DateTimeField(null=True, blank=True)
    last_checked = models.DateTimeField(auto_now=True)
    resolved = models.BooleanField(default=False)
    resolved_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return "{} - {} - {} - {}".format(self.store.store_number, self.get_issue_display(), self.down_since, self.is_active())
        
    def is_active(self):
        if self.resolved:
            return 'Resolved'
        return 'Unresolved'
        
    def total_time_down(self):
        if self.resolved is False:
            return (timezone.now() - self.down_since).total_seconds()
        return (self.resolved_time - self.down_since).total_seconds
        
    @property
    def icon(self):
        color = 'red'
        time_threshold = datetime.now() - timedelta(minutes=5)
        workon = WorkOn.objects.filter(issue_id=self, work_on_at__lt=time_threshold).last()
        if workon is not None:
            color = 'blue'
        elif self.ticket is not None:
            color = 'purple'
        return [color, self.issue]
        
        
    
    @property    
    def workon(self):
        return WorkOn.objects.filter(issue_id=self).last()
    
    @property    
    def circuits(self): 
        return Circuit.objects.filter(store__store_number=self.store.store_number,circuit_type='P').last()
        
        
class WorkOn(models.Model):
    issue_id = models.ForeignKey('CommunicationsIssue')
    work_on_by = models.ForeignKey(User)
    work_on_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '{0} working on {1}-{2} for store {3} at {4}'.format(
            self.work_on_by,
            self.issue_id.pk,
            self.issue_id.get_issue_display(),
            self.issue_id.store.store_number, 
            self.work_on_at
            )
            
            
            
            

