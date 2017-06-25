from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField, PrimaryKeyRelatedField

from phones.models import *

class PhoneBillingListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='store-phone-detail', lookup_field='pk')
    
    class Meta:
        model = PhoneBilling
        fields = ('pk', 'url')
        
class PhoneBillingDetailSerializer(ModelSerializer):
    district_url = HyperlinkedIdentityField(
        view_name='store-phone-detail', 
        lookup_field='pk',
        lookup_url_kwarg = 'pk'
    )

    class Meta:
        model = PhoneBilling
        fields = '__all__'