from django.db import models

from locations.models import DistrbutionCenter, Store


class System(models.Model):
    dc = models.ForeignKey(DistrbutionCenter, blank=True, null=True)
    router_at_store = models.ForeignKey(Store, blank=True, null=True)
    location_type = models.CharField(max_length=20, choices=(('Router', 'Router'), ('DC', 'DC')))
    status = models.CharField(max_length=5, choices=(('UP', 'UP'),('DOWN', 'DOWN')))
    
    
class SystemIP(models.Model):
    system = models.ForeignKey(System)
    ip = models.GenericIPAddressField()
    device_type = models.CharField(max_length=20, choices=(('Router', 'Router'), ('AS400', 'AS400')))
    device_location = models.CharField(max_length=60)
    status = models.CharField(max_length=5, choices=(('UP', 'UP'),('DOWN', 'DOWN')))
    
    
class DownHistory(models.Model):
    system = models.ForeignKey(System)
    down_at = models.DateTimeField()
    up_at = models.DateTimeField()
    ticket_number = models.CharField(max_length=20)