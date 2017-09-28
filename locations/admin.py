from django.contrib import admin

from .models import Store, District, Region, Division, DistributionCenter, DMA

# Register your models here.

admin.site.register(Store)
admin.site.register(District)
admin.site.register(Region)
admin.site.register(Division)
admin.site.register(DistributionCenter)
admin.site.register(DMA)