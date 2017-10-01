from django.contrib import admin

# Register your models here
from .models import System, SystemIP, DownHistory

admin.site.register(System)
admin.site.register(SystemIP)
admin.site.register(DownHistory)
