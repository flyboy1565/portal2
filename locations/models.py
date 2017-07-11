# django 
from django.db import models

# third party
from localflavor.us.models import USStateField
from localflavor.us.us_states import STATE_CHOICES
from auditlog.registry import auditlog

# my helpers
from locations.choices import location_status


class Store(models.Model):
    store_number = models.IntegerField(primary_key=True)
    three_letter_code = models.CharField(max_length=3, blank=True, null=True)
    system_name = models.CharField(max_length=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    latitude = models.DecimalField(max_digits=11, decimal_places=8)
    address = models.CharField(max_length=60, blank=True, null=True)
    city = models.CharField(max_length=60, blank=True, null=True)
    state = USStateField(choices = STATE_CHOICES)
    zip_code = models.CharField(max_length=5, blank=True, null=True)
    district = models.ForeignKey('District', blank=True, null=True)
    dma = models.ForeignKey('DMA', blank=True, null=True)
    dc = models.ForeignKey('DistrbutionCenter', blank=True, null=True)
    priority = models.BooleanField(default=False)
    hub = models.CharField(max_length=4, blank=True, null=True)
    is_hub = models.BooleanField(default=False)
    previous_year_sales = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    open_date = models.DateField(blank=True, null=True)
    close_date = models.DateField(blank=True, null=True)
    weekday_open = models.TimeField(blank=True, null=True)
    weekday_close = models.TimeField(blank=True, null=True)
    sat_open = models.TimeField(blank=True, null=True)
    sat_close = models.TimeField(blank=True, null=True)
    sun_open = models.TimeField(blank=True, null=True)
    sun_close = models.TimeField(blank=True, null=True)
    timezone = models.CharField(max_length=4, blank=True, null=True)
    full_timezone = models.CharField(max_length=50, blank=True, null=True)
    bond = models.BooleanField(default=False)
    store_status = models.CharField(max_length=20, choices=location_status())
    
    def __str__(self):
        return "{}".format(self.store_number)
    

class District(models.Model):
    district_number = models.IntegerField(primary_key=True)
    manager_name = models.CharField(max_length=100, blank=True, null=True)
    connected_to_store = models.ForeignKey('Store', blank=True, null=True, related_name='district_off_store')
    region = models.ForeignKey('Region', blank=True, null=True)
    district_status = models.CharField(max_length=20, choices=location_status())
    
    def __str__(self):
        return "{}".format(self.district_number)

    
class Region(models.Model):
    region_number = models.IntegerField(primary_key=True)
    manager_name = models.CharField(max_length=100, blank=True, null=True)
    connected_to_store = models.ForeignKey('Store', blank=True, null=True, related_name='region_off_store')
    division = models.ForeignKey('Division', blank=True, null=True)
    region_status = models.CharField(max_length=20, choices=location_status())
    
    def __str__(self):
        return "{}".format(self.region_number)
        
        
class Division(models.Model):
    division_number = models.IntegerField(primary_key=True)
    manager_name = models.CharField(max_length=100, blank=True, null=True)
    connected_to_store = models.ForeignKey('Store', blank=True, null=True, related_name='division_off_store')
    division_status = models.CharField(max_length=20, choices=location_status())
    
    def __str__(self):
        return "{}".format(self.division_number)
        

class DistrbutionCenter(models.Model):
    dc_number = models.IntegerField(primary_key=True)
    manager_name = models.CharField(max_length=100, blank=True, null=True)
    store_off_dc = models.ForeignKey('Store', blank=True, null=True)        
    dc_status = models.CharField(max_length=20, choices=location_status())
    
    def __str__(self):
        return "{}".format(self.dc_number)
        

class DMA(models.Model):
    dma_number = models.IntegerField(primary_key=True)
    
    def __str__(self):
        return "{}".format(self.dma_number)
        

auditlog.register(Store)
auditlog.register(District)
auditlog.register(Region)
auditlog.register(Division)
auditlog.register(DistrbutionCenter)
auditlog.register(DMA)