from django.shortcuts import render

# Create your views here.
from .models import System, SystemIP, DownHistory


def get_all(request):
    devices = System.objects.all()
    return render(request, 'devices/all_devices.html', {'devices':devices})
    
def get_one(request, id):
    system = System.objects.get(dc__dc_number=id)
    if not system:
        system = System.objects.get(router_at_store__store_number=id)
    ips = SystemIP.objects.filter(system=system)
    return render(request, 'devices/device.html', {'ips':ips})