from rest_framework.serializers import (
            ModelSerializer, HyperlinkedIdentityField, 
            SerializerMethodField, PrimaryKeyRelatedField
        )
        
from devices.models import System, SystemIP, DownHistory
from locations.models import DistributionCenter, Store
from cdks.api.serializers import StoreSerializer


class DistributionCenterSerializer(ModelSerializer):
    
    class Meta:
        model = DistributionCenter
        fields = ('dc_number', 'longitude', 'latitude')
        lookup_field = 'dc_number'
        
        
class SystemListSerializer(ModelSerializer):
    location = SerializerMethodField()
    
    class Meta:
        model = System
        fields = '__all__'
        
    def get_location(self, obj):
        print(obj)
        if obj.dc:
            dc = DistributionCenter.objects.get(dc_number=str(obj.dc))
            serializer = DistributionCenterSerializer(instance=dc)
            return serializer.data
        if obj.router_at_store:
            store = Store.objects.get(store_number=str(obj.router_at_store))
            serializer = StoreSerializer(instance=store)
            return serializer.data