from django.shortcuts import render

from .models import CommunicationsIssue

def infowindow(request, id):
    issue = CommunicationsIssue.objects.get(pk=id)
    context = {'issue': issue}
    return render(request, 'infowindow.html', context)