from django.shortcuts import render

# Create your views here.
from .models import System, SystemIP, DownHistory


def get_all(request):
    System = Kit.objects.all()
    print(kits)
    return render(request, 'cdks/all_kits.html', {'kits':kits})
    
def get_one(request, id):
    kit = System.objects.get(pk=id)
    return render(request, 'cdks/all_kits.html', {'kits':kit})