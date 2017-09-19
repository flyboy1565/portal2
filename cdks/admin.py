from django.contrib import admin

# Register your models here.
from .models import Kit, Shipping

admin.site.register(Kit)
admin.site.register(Shipping)