from django.shortcuts import render
from django.http import JsonResponse

from .models import CommunicationsIssue
from locations.models import Store, DistributionCenter
from phones.models import PhoneLine

from .forms import EditIssueForm

def infowindow(request, id):
    issue = CommunicationsIssue.objects.get(pk=id)
    pots = issue.store.phoneline_set.select_related().filter(phone_type='PTS').first()
    circuit = issue.store.circuit_set.select_related().filter(circuit_type='P').first()
    context = {'issue': issue, 'pots': pots, 'circuit': circuit}
    return render(request, 'issues/infowindow.html', context)
    
    
def store_search(request, store):
    if int(store) < 100:
        print('DC Search')
    else:
        try:
            store = Store.objects.get(store_number=store)
            phones = PhoneLine.objects.filter(store=store)
        except Store.DoesNotExist:
           store = None
           phones = None
    return render(request, 'issues/search_data.html', {'store': store, 'phones': phones})
    
    
def edit_issue(request, id=None):
    if id is None:
        pk = request.POST.get('pk')
        issue_type = request.POST.get('issue_id')
        issue = CommunicationsIssue.objects.get(pk=pk)
        issue.issue = issue_type
        issue.save()
        return JsonResponse({'issue': 'issue editted'})
    else:
        issue = CommunicationsIssue.objects.get(pk=id)
        form = EditIssueForm(initial={'pk': issue.pk, 'issue': issue.issue})
        return render(request, 'issues/edit_issue_form.html', {'form': form})