from django.shortcuts import render
from django.utils import timezone

# Create your views here.
from .models import Store

def new_stores(request):
    stores = Store.objects.filter(open_date__gt=timezone.now())