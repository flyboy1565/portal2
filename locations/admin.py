from django.contrib import admin

from .models import Store, District, Region, Division, DistrbutionCenter, DMA

# Register your models here.

admin.site.register(Store)
admin.site.register(District)
admin.site.register(Region)
admin.site.register(Division)
admin.site.register(DistrbutionCenter)
admin.site.register(DMA)