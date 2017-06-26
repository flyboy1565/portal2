from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField, PrimaryKeyRelatedField

from phones.models import *


class PhoneBillingListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='store-phone-detail', lookup_field='store_number')
    
    class Meta:
        model = PhoneBilling
        fields = ('store_number', 'url')
        
        
class PhoneBillingDetailSerializer(ModelSerializer):

    class Meta:
        model = PhoneBilling
        fields = '__all__'