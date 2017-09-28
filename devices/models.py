from django.db import models

from locations.models import DistributionCenter, Store


class System(models.Model):
    dc = models.ForeignKey(DistributionCenter, blank=True, null=True)
    router_at_store = models.ForeignKey(Store, blank=True, null=True)
    location_type = models.CharField(max_length=20, choices=(('Router', 'Router'), ('DC', 'DC')))
    status = models.CharField(max_length=5, choices=(('UP', 'UP'),('DOWN', 'DOWN')))
    
    def __str__(self):
        if self.dc:
            return str(self.dc.dc_number)
        elif self.router_at_store:
            return str(self.router_at_store.store_number)
            
    class Meta:
        verbose_name_plural = "Systems"
    
    
class SystemIP(models.Model):
    system = models.ForeignKey(System)
    ip = models.GenericIPAddressField(protocol='IPv4')
    device_type = models.CharField(max_length=20, choices=(('Router', 'Router'), ('AS400', 'AS400')))
    device_location = models.CharField(max_length=60)
    status = models.CharField(max_length=5, choices=(('UP', 'UP'),('DOWN', 'DOWN')))
    
    def __str__(self):
        return "{}-{}".format(self.system, self.get_device_type_display())
        
    class Meta:
        verbose_name_plural = "System IPs"
    
    
class DownHistory(models.Model):
    system = models.ForeignKey(System)
    down_at = models.DateTimeField()
    up_at = models.DateTimeField()
    ticket_number = models.CharField(max_length=20)
    
    class Meta:
        verbose_name_plural = "Down Histories"