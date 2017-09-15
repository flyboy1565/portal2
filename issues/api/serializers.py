from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField, PrimaryKeyRelatedField

from issues.models import CommunicationsIssue, WorkOn
# from .views import UpdateIssueWithWorkOn
from locations.models import Store
from circuits.models import Circuit
from rest_framework.fields import CurrentUserDefault


class StoreSerializer(ModelSerializer):
    
    class Meta:
        model = Store
        fields = ('store_number', 'longitude', 'latitude', 'state')
        lookup_field = 'store_number'
        
        
class CircuitSerializer(ModelSerializer):
    circuit_type = SerializerMethodField()
    vendor_name = SerializerMethodField()
    communications_type = SerializerMethodField()
    
    class Meta:
        model = Circuit
        fields = ('circuit_turn_up','circuit_type', 'communications_type', 'id','vendor_name')
        lookup_field = 'id__store__store_number'
        
    def get_circuit_type(self, obj):
        return obj.get_circuit_type_display()
        
    def get_vendor_name(self, obj):
        return obj.primary_vendor.vendor_name
        
    def get_communications_type(self, obj):
        return obj.communications_type.comm_type
        
        
class WorkOnSerializer(ModelSerializer):
    work_on_user = SerializerMethodField()
    
    class Meta:
        model = WorkOn
        fields = '__all__'
        lookup_field = 'issue_id__store__store_number'
        
    def get_work_on_user(self, obj):
        return obj.work_on_by.get_full_name()
            

class IssueListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='issue-detail', lookup_field='id')
    store = StoreSerializer()
    workon = WorkOnSerializer()
    circuits = CircuitSerializer()
    icon = SerializerMethodField(source='icon')
    
    class Meta:
        model = CommunicationsIssue
        fields = '__all__'
        
    def get_icon(self, obj):
        return obj.icon
        
        
class IssueDetailSerializer(ModelSerializer):
    store = StoreSerializer()
    
    class Meta:
        model = CommunicationsIssue
        fields = '__all__'
        

class IssueSerializer(ModelSerializer):
    store = StoreSerializer()
    workon = WorkOnSerializer()
    circuits = CircuitSerializer()
    icon = SerializerMethodField(source='icon')
    
    class Meta:
        model = CommunicationsIssue
        fields = '__all__'
        lookup_field = 'issue_id__store__store_number'
    
    def get_icon(self, obj):
        return obj.icon
        