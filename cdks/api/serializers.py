from rest_framework.serializers import (
            ModelSerializer, HyperlinkedIdentityField, 
            SerializerMethodField, PrimaryKeyRelatedField
        )

from cdks.models import Kit, Shipping

from locations.models import Store


class StoreSerializer(ModelSerializer):
    
    class Meta:
        model = Store
        fields = ('store_number', 'longitude', 'latitude', 'state')
        lookup_field = 'store_number'


class ShippingDetailSerializer(ModelSerializer):
    
    class Meta:
        model = Shipping
        fields = '__all__'
        


class KitListSerializer(ModelSerializer):
    shipping = ShippingDetailSerializer()
    store = SerializerMethodField()
    
    class Meta:
        model = Kit
        fields = '__all__'
        
    def get_store(self, obj):
        print(obj.shipping)
        if obj.shipping:
            store = Store.objects.filter(store_number=str(obj.shipping.at_store))
            serializer = StoreSerializer(instance=store, many=True)
            return serializer.data
        return {}
    