from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView

from locations.models import Store, District, Region, Division, DistrbutionCenter, DMA

from .serializers import (
        StoreListSerializer, StoreDetailSerializer,
        DistrictListSerializer, DistrictDetailSerializer,
        RegionListSerializer, RegionDetailSerializer,
        DivisionListSerializer, DivisionDetailSerializer,
        DistrbutionCenterListSerializer, DistrbutionCenterDetailSerializer,
)


class StoreDetailAPIView(RetrieveAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreDetailSerializer
    lookup_field = 'store_number'


class StoreListAPIView(ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreListSerializer
    
    
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
    serializer_class = DivisionListSerializer
    

class DivisionDetailAPIView(RetrieveAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionDetailSerializer
    lookup_field = 'division_number'
    
    
class DistrbutionCenterListAPIView(ListAPIView):
    queryset = DistrbutionCenter.objects.all()
    serializer_class = DistrbutionCenterListSerializer
    

class DistrbutionCenterDetailAPIView(RetrieveAPIView):
    queryset = DistrbutionCenter.objects.all()
    serializer_class = DistrbutionCenterDetailSerializer
    lookup_field = 'dc_number'