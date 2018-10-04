import numbers
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

from locations.models import Store, DistributionCenter
from circuits.models import Circuit
from phones.models import PhoneLine

from .choices import issues_choices


def system_choices():
    systems = [('All Stores', 'All Stores'), ('All DCs', 'All DCs')]
    try:
        for store in Store.objects.all():
            systems.append((str(store.store_number), str(store.store_number)))
        for dc in DistributionCenter.objects.all():
            systems.append((str(dc.dc_number), str(dc.dc_number)))
    except:
        pass
    print(systems)
    return systems


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
            total = (self.down_since - timezone.now()).total_seconds()
        else:
            total = (self.down_since - self.resolved_time).total_seconds()
        return self.humanize_time(total)
        
    def humanize_time(self, secs):
        mins, secs = divmod(secs, 60)
        hours, mins = divmod(mins, 60)
        if hours > 0:
            return '%02d minutes %02d seconds' % (mins, secs)
        return '%02d hours %02d minutes' % (hours, mins)
        
    @property
    def icon(self):
        color = 'red'
        time_threshold = timezone.now() - timedelta(minutes=5)
        workon = WorkOn.objects.filter(issue_id=self, work_on_at__lt=time_threshold, completed=False).last()
        if workon is not None:
            color = 'blue'
        elif self.ticket is not None:
            color = 'purple'
        if self.issue == 'PC':
            self.issue = 'C'
        return [color, self.issue]
        
    @property    
    def workon(self):
        time_threshold = timezone.now() - timedelta(minutes=5)
        print(time_threshold)
        now = timezone.now()
        print(now)
        return WorkOn.objects.filter(issue_id=self, work_on_at__range=(time_threshold, now), completed=False).last()
    
    @property    
    def circuits(self): 
        return Circuit.objects.filter(store__store_number=self.store.store_number,circuit_type='P').last()
        
    @property
    def phone(self):
        return PhoneLine.objects.filter(store__store_number=self.store.store_number,phone_type='S').first()
        

class AdditionalIssue(models.Model):
    description = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=(('Monitoring', 'Monitoring'), ('Active', 'Active')))
    expires_at = models.DateTimeField(blank=True, null=False)
    date_added = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User)
    effected_systems = models.CharField(max_length=50, choices=system_choices())
    ticket_number = models.CharField(max_length=50)
    closed = models.BooleanField(default=False)
    
        
class WorkOn(models.Model):
    issue_id = models.ForeignKey('CommunicationsIssue')
    work_on_by = models.ForeignKey(User)
    work_on_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return '{0} working on {1}-{2} for store {3} at {4}'.format(
            self.work_on_by,
            self.issue_id.pk,
            self.issue_id.get_issue_display(),
            self.issue_id.store.store_number, 
            self.work_on_at
            )
            
            
            
            
            

