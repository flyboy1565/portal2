from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView

from issues.models import CommunicationsIssue

from .serializers import (
        IssueListSerializer, IssueDetailSerializer,
)


class IssueDetailAPIView(RetrieveAPIView):
    queryset = CommunicationsIssue.objects.all()
    serializer_class = IssueDetailSerializer
    lookup_field = 'id'


class IssueListAPIView(ListAPIView):
    queryset = CommunicationsIssue.objects.filter(resolved=False)
    serializer_class = IssueListSerializer
    