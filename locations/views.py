from django.shortcuts import render
from django.utils import timezone

# Create your views here.
from .models import Store

def new_stores(request):
    stores = Store.objects.filter(open_date__gt=timezone.now())
    
    
def deactivated_stores(request):
    stores = Store.objects.exclude(store_status='Open')
    context = {'stores': stores,}
    return render(request, 'issues/reports/deactivated_report.html', context)
    