from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Kit, Shipping
from .forms import NewKit, ShipKit

from vendors.models import Vendor
from locations.models import Store

def get_all(request):
    kits = Kit.objects.all()
    return render(request, 'cdks/all_kits.html', {'kits':kits})
    
    
def get_one(request, id):
    kit = Kit.objects.get(pk=id)
    shipments = Shipping.objects.filter(kit_shipped=kit)
    return render(request, 'cdks/kit_detail.html', {'kit':kit, 'shipments': shipments})
    
    
def create_new(request):
    if request.POST:
        vendor = Vendor.objects.get(pk=request.POST.get('id_carrier'))
        kit = Kit()
        kit.kit_number = request.POST.get('id_kit_number')
        kit.carrier = vendor
        kit.modem_ip = request.POST.get('id_modem_ip')
        kit.modem_serial_number = request.POST.get('id_modem_serial_number')
        kit.cisco_serial_number = request.POST.get('id_cisco_serial_number')
        kit.imei = request.POST.get('id_imei')
        kit.tunnel_200 = request.POST.get('id_tunnel_200')
        kit.tunnel_500 = request.POST.get('id_tunnel_500')
        kit.status = 'Active'
        kit.save()
        return JsonResponse({"status": 'worked'})
    else:
        form = NewKit()
        return render(request, 'cdks/new_kit.html', {'form': form})
        
        
def new_shipment(request, id):
    if request.POST:
        kit = Kit.objects.get(pk=id)
        store = Store.objects.get(pk=request.POST.get('store'))
        s = Shipping()
        s.at_store = store
        s.kit_shipped = kit
        s.ticket_number = request.POST.get('ticket')
        s.shipped_date = timezone.now().date()
        s.tracking_number_to_store = request.POST.get('to_store')
        s.tracking_number_to_help_support = request.POST.get('to_hs')
        s.save()
        return JsonResponse({"status": 'worked'})
    else:
        kit = Kit.objects.get(pk=id)
        form = ShipKit()
        return render(request, 'cdks/ship_kit.html', {'form': form, 'kit':kit})
        

def return_shipment(request, id):
    print(request.POST)
    print(id)
    if request.POST:
        shipment = Shipping.objects.get(pk=id)
        print(request.user)
        user = User.objects.get(username=request.user)
        shipment.returned_on = timezone.now().date()
        shipment.returned_accept_by = user
        shipment.status = 'Returned'
        shipment.save()
        return JsonResponse({'status': 'worked'})
    return JsonResponse({'status': 'Not using POST!'})
    

def lost_shipment(request, id):
    if request.POST:
        print(id)
        kit = Kit.objects.get(pk=id)
        user = User.objects.get(username=request.user)
        kit.shipping.returned_on = timezone.now().date()
        kit.shipping.returned_accept_by = user
        kit.shipping.status = 'Returned'
        kit.shipping.save()
        kit.status = 'Lost'
        kit.save()
        return JsonResponse({'status': 'worked'})
    return JsonResponse({'status': 'Not using POST!'})
    
    
def add_tracking(request, kit_id, ship_type):
    if request.POST:
        shipment = Kit.objects.get(pk=kit_id).shipping
        if ship_type == 'to_store':
            shipment.tracking_number_to_store = request.POST.get('tracking_number')
        else:
            shipment.tracking_number_to_help_support = request.POST.get('tracking_number')
        shipment.save()
        return JsonResponse({'status': 'worked'})
    return JsonResponse({'status': 'Not using POST!'})
    
    
def request_return(request, kit_id):
    if request.POST:
        shipment = Kit.objects.get(pk=kit_id).shipping
        shipment.return_requested_on = timezone.now().date()
        shipment.save()
        return JsonResponse({'status': 'worked'})
    return JsonResponse({'status': 'Not using POST!'})