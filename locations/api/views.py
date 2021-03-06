from django.utils import timezone

from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView

from locations.models import Store, District, Region, Division, DistributionCenter, DMA

from .serializers import (
        StoreListSerializer, StoreDetailSerializer,
        DistrictListSerializer, DistrictDetailSerializer,
        RegionListSerializer, RegionDetailSerializer,
        DivisionListSerializer, DivisionDetailSerializer,
        NewStoreListSerializer,
)


class StoreDetailAPIView(RetrieveAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreDetailSerializer
    lookup_field = 'store_number'


class StoreListAPIView(ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreListSerializer
    

class NewStoreListAPIView(ListAPIView):
    queryset = Store.objects.filter(open_date__gt=timezone.now())
    serializer_class = NewStoreListSerializer
    

class DistrictDetailAPIView(RetrieveAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictDetailSerializer
    lookup_field = 'district_number'


class DistrictListAPIView(ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictListSerializer
    
    
class RegionListAPIView(ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionListSerializer

class RegionDetailAPIView(RetrieveAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionDetailSerializer
    lookup_field = 'region_number'
    
    
class DivisionListAPIView(ListAPIView):
    queryset = Division.objects.all()
    serializer_class = RegionListSerializer

class DivisionDetailAPIView(RetrieveAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionDetailSerializer
    lookup_field = 'division_number'
    
