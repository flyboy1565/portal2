from django.shortcuts import render

from .models import Kit

def get_all(request):
    kits = Kit.objects.all()
    print(kits)
    return render(request, 'cdks/all_kits.html', {'kits':kits})
    
def get_one(request, id):
    kit = Kit.objects.get(pk=id)
    return render(request, 'cdks/all_kits.html', {'kits':kit})