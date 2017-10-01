from django.db import models

from locations.models import Store, DistributionCenter
from vendors.models import Vendor
from django.contrib.auth.models import User


class Kit(models.Model):
    kit_number = models.PositiveIntegerField(unique=True)
    carrier = models.ForeignKey(Vendor)
    modem_ip = models.GenericIPAddressField(protocol='IPv4')
    modem_serial_number = models.CharField(max_length=50)
    cisco_serial_number = models.CharField(max_length=50)
    imei = models.CharField(max_length=50)
    tunnel_200 = models.GenericIPAddressField(protocol='IPv4')
    tunnel_500 = models.GenericIPAddressField(protocol='IPv4')
    online =  models.BooleanField(default=False)
    status = models.CharField(max_length=30, choices=(('Active', 'Active'), ('Deactivated', 'Deactivated'), ('Lost', 'Lost')), default='Active')
    
    def __str__(self):
        return "{}".format(self.kit_number)
    
    @property
    def shipping(self):
        if self.status == 'Lost':
            return None
        result = Shipping.objects.filter(kit_shipped=self.kit_number).last()
        return result
        

class Shipping(models.Model):
    at_store = models.ForeignKey(Store)
    kit_shipped = models.ForeignKey(Kit)
    ticket_number = models.CharField(max_length=20)
    shipped_date = models.DateField()
    tracking_number_to_store = models.CharField(max_length=20)
    tracking_number_to_help_support = models.CharField(max_length=20, blank=True, null=True)
    return_requested_on = models.DateField(blank=True, null=True)
    returned_on = models.DateField(blank=True, null=True)
    returned_accept_by = models.ForeignKey(User, blank=True, null=True)
    status = models.CharField(max_length=30, choices=(('Returned', 'Returned'), ('At Store', 'At Store')), default='At Store')
    
    def __str__(self):
        return "{}. Kit #{}".format(self.pk, self.kit_shipped)
    
