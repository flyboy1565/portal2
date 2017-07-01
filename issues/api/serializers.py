from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField, PrimaryKeyRelatedField

from issues.models import CommunicationsIssue

class IssueListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='issue-detail', lookup_field='id')
    
    class Meta:
        model = CommunicationsIssue
        fields = ('store', 'id', 'url')
        
class IssueDetailSerializer(ModelSerializer):
    
    class Meta:
        model = CommunicationsIssue
        fields = '__all__'