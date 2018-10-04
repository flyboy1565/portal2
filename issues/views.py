from datetime import datetime, timedelta

from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User

from .models import CommunicationsIssue, AdditionalIssue
from locations.models import Store, DistributionCenter
from circuits.models import Circuit
from phones.models import PhoneLine

from .forms import EditIssueForm, AdditionalIssueForm


def infowindow(request, id):
    issue = CommunicationsIssue.objects.get(pk=id)
    try:
        pots = issue.store.phoneline_set.select_related().filter(phone_type='PTS').first()
    except:
        pots = None
    try:
        circuit = issue.store.circuit_set.select_related().filter(circuit_type='P').first()
    except:
        circuit = None
    context = {'issue': issue, 'pots': pots, 'circuit': circuit}
    return render(request, 'issues/infowindow.html', context)
    
    
def store_search(request, store):
    if int(store) < 100:
        print('DC Search')
    else:
        try:
            store = Store.objects.get(store_number=store)
        except Store.DoesNotExist:
           store = None
        try:
            print(store)
            phones = PhoneLine.objects.filter(store=store.phone_billing_store)
        except: 
            phones = None
        try:
            circuit = Circuit.objects.filter(circuit_type='P').first()
        except:
            circuit = None
    context = {'store': store, 'phones': phones, 'circuit':circuit}
    print(context)
    return render(request, 'issues/search_data.html', context)
    
    
def edit_issue(request, id=None):
    if id is None:
        pk = request.POST.get('pk')
        issue = CommunicationsIssue.objects.get(pk=pk)
        issue.issue = request.POST.get('issue_id')
        issue.save()
        return JsonResponse({'issue': 'issue editted'})
    else:
        issue = CommunicationsIssue.objects.get(pk=id)
        form = EditIssueForm(initial={'pk': issue.pk, 'issue': issue.issue})
        return render(request, 'issues/edit_issue_form.html', {'form': form})
        

def deactivate_store(request, store):
    user = User.objects.get(username=request.user)
    if user.profile.shsg:
        store = Store.objects.get(store_number=store)
        print(store.store_status)
        if store.store_status != 'Open':
            store.store_status = 'Open'
        else:
            store.store_status = 'Closed'
        store.save()
        print(store.store_status)
        return JsonResponse({"update": "deactivated", 'status': store.store_status})
    return JsonResponse({"update": "not_authorized"})
    
    
def additional_issues(request):
    issues = AdditionalIssue.objects.filter(closed=False, expires_at__gt=timezone.now())
    return render(request, 'issues/additional_issues.html', {'issues': issues})


def new_additional_issue(request):
    if request.POST:
        new = AdditionalIssue()
        user = User.objects.get(username=request.user)
        new.description = request.POST.get('description')
        new.expires_at = request.POST.get('expires_at')
        new.effected_systems = request.POST.get('effected_systems')
        new.ticket_number = request.POST.get('ticket_number')
        new.added_by = user
        new.save()
        return JsonResponse({'status': 'worked'})
    else:
        form = AdditionalIssueForm()
        return render(request, 'issues/new_additional_issue.html', {'form': form})
        
        
def close_additional(request, id):
    issue = AdditionalIssue.objects.get(pk=id)
    issue.closed = True
    issue.save()
    return JsonResponse({'status': 'worked'})        
    
    
def report_total_down(request):
    today = timezone.now() 
    previous = today - timedelta(days=1)
    issues = CommunicationsIssue.objects.filter(down_since__range=[previous, today])
    return render(request, 'issues/reports/total_down.html', {'issues': issues})
    
    
