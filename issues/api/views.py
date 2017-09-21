from django.http import JsonResponse
from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView

from issues.models import CommunicationsIssue, WorkOn, User

from .serializers import ( IssueListSerializer, IssueSerializer, IssueDetailSerializer )


class IssueDetailAPIView(RetrieveAPIView):
    queryset = CommunicationsIssue.objects.all()
    serializer_class = IssueDetailSerializer
    lookup_field = 'id'


class IssueListAPIView(ListAPIView):
    queryset = CommunicationsIssue.objects.filter(resolved=False)
    serializer_class = IssueListSerializer
    

def UpdateIssueWithWorkOn(request, id):
    user = User.objects.get(username=request.user)
    issue = CommunicationsIssue.objects.get(pk=id)
    print(user)
    print(issue)
    work_on = WorkOn()
    work_on.issue_id = issue
    work_on.work_on_by = user
    work_on.save()
    return JsonResponse(IssueSerializer(issue).data)
    

def WorkOnCompleted(request, id):
    issue = CommunicationsIssue.objects.get(pk=id)
    work_on = WorkOn.objects.filter(issue_id=issue).last()
    work_on.completed = True
    work_on.save()
    return JsonResponse(IssueSerializer(issue).data)
    
    