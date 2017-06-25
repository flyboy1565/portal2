from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField, PrimaryKeyRelatedField

from locations.models import  Store, District, Region, Division, DistrbutionCenter, DMA


class StoreListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='store-detail', lookup_field='store_number')
    
    class Meta:
        model = Store
        fields = ('store_number', 'url')
        
class StoreDetailSerializer(ModelSerializer):
    district_url = HyperlinkedIdentityField(
        view_name='district-detail', 
        lookup_field='district',
        lookup_url_kwarg = 'district_number'
    )

    class Meta:
        model = Store
        fields = '__all__'
        
class DistrictListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='district-detail', lookup_field='district_number')
    
    class Meta:
        model = District
        fields = '__all__'
        
class DistrictDetailSerializer(ModelSerializer):
    stores = SerializerMethodField()

    class Meta:
        model = District
        fields = '__all__'
    
    def get_stores(self, obj):
        queryset = Store.objects.filter(district=obj.district_number)
        return StoreListSerializer(queryset, many=True, context=self.context).data
        
        
class RegionListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='region-detail', lookup_field='region_number')
    
    class Meta:
        model = Region
        fields = '__all__'
        
        
class RegionDetailSerializer(ModelSerializer):
    districts = SerializerMethodField()
    
    class Meta:
        model = Region
        fields = '__all__'
    
    def get_districts(self, obj):
        queryset = District.objects.filter(region=obj.region_number)
        return DistrictListSerializer(queryset, many=True, context=self.context).data
        
    
class DivisionListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='region-detail', lookup_field='region_number')
    
    class Meta:
        model = Region
        fields = '__all__'
        
        
class DivisionDetailSerializer(ModelSerializer):
    regions = SerializerMethodField()
    
    class Meta:
        model = Region
        fields = '__all__'
    
    def get_regions(self, obj):
        queryset = Region.objects.filter(division=obj.division_number)
        return DistrictListSerializer(queryset, many=True, context=self.context).data  