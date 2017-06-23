from django.db import models

from choices import location_status
# Create your models here.

class Store(models.Model):
    store = models.IntegerField(primary_key=True)
    three_letter_code = models.CharField(max_length=3, blank=True, null=True)
    system_name = models.CharField(max_length=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    latitude = models.DecimalField(max_digits=11, decimal_places=8)
    address = models.CharField(max_length=60, blank=True, null=True)
    city = models.CharField(max_length=60, blank=True, null=True)
    state = models.CharField(max_length=60, blank=True, null=True)
    zip_code = models.CharField(max_length=5, blank=True, null=True)
    district = models.ForeignKey('District', blank=True, null=True)
    dma = models.ForeignKey('DMA', blank=True, null=True)
    dc = models.ForeignKey('DistrbutionCenter', blank=True, null=True)
    priority = models.IntegerField()
    hub = models.CharField(max_length=4, blank=True, null=True)
    is_hub = models.IntegerField()
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
    bond = models.BooleanField(default=True)
    store_status = models.CharField(max_length=20, choices=location_status())
    
    def __str__(self):
        return "{}".format(self.store)
    

class District(models.Model):
    district = models.IntegerField(primary_key=True)
    manager_name = models.CharField(max_length=100, blank=True, null=True)
    connected_to_store = models.ForeignKey('Store', blank=True, null=True)
    region = models.ForeignKey('Region', blank=True, null=True)
    district_status = models.CharField(max_length=20, choices=location_status())
    
    def __str__(self):
        return "{}".format(self.district)

    
class Region(models.Model):
    region = models.IntegerField(primary_key=True)
    manager_name = models.CharField(max_length=100, blank=True, null=True)
    connected_to_store = models.ForeignKey('Store', blank=True, null=True)
    region = models.ForeignKey('Region', blank=True, null=True)
    district_status = models.CharField(max_length=20, choices=location_status())
    
    def __str__(self):
        return "{}".format(self.district)
        

class DistrbutionCenter(models.Model):
    dc = models.IntegerField(primary_key=True)
    manager_name = models.CharField(max_length=100, blank=True, null=True)
    store_off_dc = models.ForeignKey('Store', blank=True, null=True)        
    dc_status = models.CharField(max_length=20, choices=location_status())
    
    def __str__(self):
        return "{}".format(self.dc)