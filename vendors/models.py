from django.db import models

# Create your models here.

class Vendor(models.Model):
    vendor_name = models.CharField(max_length=30)
    base_emails = models.ManyToManyField('VendorEmail', blank=True, related_name='vendor_base_emails')
    notes = models.CharField(max_length=200)
    
    def __str__(self):
        return self.vendor_name
        
        
class VendorEmail(models.Model):
    vendor = models.ForeignKey(Vendor, related_name='vendor_email_name')
    email_address = models.EmailField()
    active = models.BooleanField(default=True)
    
    def is_active(self):
        if self.active:
            return 'is active'
        return 'is not active'
    
    def __str__(self):
        return "Email ({}) for {} {}".format(self.email_address, self.vendor.vendor_name, self.is_active())