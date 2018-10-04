from django.db import models
from django.contrib.auth.models import User

from localflavor.us.models import PhoneNumberField
from auditlog.registry import auditlog
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from locations.models import Store
from vendors.models import Vendor
from .choices import phone_types, note_types, account_types, stick_types


class PhoneTag(models.Model):
    tag = models.CharField(max_length=5)
    description = models.CharField(max_length=50)
    
    def __str__(self):
        return self.tag
        

class PhoneLine(models.Model):
    store = models.ForeignKey('PhoneBilling')
    line_number = models.PositiveIntegerField()
    phone_number = PhoneNumberField(unique=True)
    tag =  models.ManyToManyField('PhoneTag')
    phone_type = models.CharField(max_length=3, choices=phone_types())
    
    def __str__(self):
        return '{} - {} - {}'.format(self.store.store_number, self.line_number, self.phone_number)
        

class PhoneEquipment(models.Model):
    phone_equipment = models.CharField(max_length=100)
    warranty_in_months = models.IntegerField(default=24)
    
    def __str__(self):
        return self.phone_equipment
    
    
class PhoneType(models.Model):
    phone_type = models.CharField(max_length=50)
    
    def __str__(self):
        return self.phone_type
        

class Carrier(models.Model):
    carrier_name = models.ForeignKey(Vendor)
    phone_number = PhoneNumberField()
    email = models.EmailField()
    
    def __str__(self):
        return self.carrier_name.vendor_name
    

class Comment(models.Model):
    store = models.ForeignKey('PhoneBilling')
    note = models.TextField(max_length=500)
    note_type = models.CharField(max_length=10, choices=note_types())
    user = models.ForeignKey(User)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{}".format(self.store.store.store_number)
    

class BillingAccountNumber(models.Model):
    account_number = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=10, choices=account_types())
    
    def __str__(self):
        return '{} - {}'.format(self.account_number, self.description)

    
class LastAudit(models.Model):
    store = models.ForeignKey('PhoneBilling')
    audit_date = models.DateTimeField(auto_now_add=True)
    audit_by = models.ForeignKey(User)
    
    def __str__(self):
        return '{} - {}'.format(self.store.store_number, self.audit_date)
        
        
class CordlessPhoneType(models.Model):
    cordless_phone = models.CharField(max_length=60)
    
    def __str__(self):
        return self.cordless_phone
    
class PhoneBilling(models.Model):
    store = models.OneToOneField(Store, related_name='phone_billing_store')
    # account numbers
    master_account_number = models.ForeignKey(BillingAccountNumber, related_name='master_account')
    secondary_account_numbers = models.ManyToManyField(BillingAccountNumber, related_name='backup_accounts')
    # monthly costs
    data_monthly = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    long_distance_monthly = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_t1_monthly = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    local_monthly = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    alarm_monthly = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    district_manager_monthly = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    regional_monthly = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # carriers
    local_exchange_carrier_1 = models.ForeignKey(Carrier, related_name='lec_1')
    local_exchange_carrier_2 = models.ForeignKey(Carrier, related_name='lec_2')
    main_data_carrier = models.ForeignKey(Carrier, related_name='main_data_carrier')
    backup_data_carrier = models.ForeignKey(Carrier, related_name='backup_data_carrier')
    data_circuit_turnup = models.DateField(blank=True, null=True)
    # phone equipment
    phone_equipment = models.ForeignKey(PhoneEquipment)
    phone_equipment_purchase_date = models.DateField(blank=True, null=True)
    phone_equipment_purchased_from = models.ForeignKey(Carrier)
    phone_type_1 = models.ForeignKey(PhoneType, related_name='phone_equipment_type_1')
    phone_type_1_number = models.IntegerField(default=0)
    phone_type_2 = models.ForeignKey(PhoneType, related_name='phone_equipment_type_2')
    phone_type_2_number = models.IntegerField(default=0)
    # Stick
    stick = models.CharField(max_length=10, choices=stick_types())
    stick_warranty_in_months = models.IntegerField(default=24)
    # Cordless
    cordless = models.ForeignKey(CordlessPhoneType,blank=True, null=True)
    cordless_warranty_in_months = models.IntegerField(default=24)
    
    @property
    def store_number(self):
        return self.store.store_number
    
    def __str__(self):
        return "{}".format(self.store.store_number)

    def audit_overdue(self):
        try:
            last_audit = LastAudit.objects.filter(store=self.pk).latest('pk')
        except:
            return True
        else:
            six_months = last_audit.audit_date + relativedelta(months=+6)
            if timezone.now() > six_months:
                return True
            else: 
                return False
        
        
auditlog.register(PhoneLine)
auditlog.register(LastAudit)
auditlog.register(Comment)
auditlog.register(PhoneBilling)

