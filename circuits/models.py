from django.db import models

from locations.models import Store
from vendors.models import Vendor

from .choices import circuit_type

class Circuit(models.Model):
    store = models.ForeignKey(Store)
    primary_vendor = models.ForeignKey(Vendor, related_name='primary_vendor')
    primary_circuit_id = models.CharField(max_length=60, blank=True, null=True)
    secondary_vendor = models.ForeignKey(Vendor, blank=True, null=True, related_name='secondary_vendor')
    secondary_circuit_id = models.CharField(max_length=60, blank=True, null=True)
    communications_type = models.ForeignKey('CommunicationsType')
    circuit_turn_up = models.DateField(blank=True, null=True)
    circuit_type = models.CharField(max_length=5, choices=circuit_type())
    
    def __str__(self):
        return "{} - {} - {}".format(self.store.store_number, self.primary_vendor.vendor_name, self.get_circuit_type_display())
    
    
class CommunicationsType(models.Model):
    comm_type = models.CharField(max_length=30, unique=True)
    
    def __str__(self):
        return self.comm_type