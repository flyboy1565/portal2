from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(PhoneTag)
admin.site.register(PhoneLine)
admin.site.register(Comment)
admin.site.register(PhoneType)
admin.site.register(PhoneEquipment)
admin.site.register(Carrier)
admin.site.register(BillingAccountNumber)
admin.site.register(LastAudit)
admin.site.register(CordlessPhoneType)
admin.site.register(PhoneBilling)
