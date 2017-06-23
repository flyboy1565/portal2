from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView

from locations.models import Store, District, Region, Division, DistrbutionCenter, DMA

from .serializers import (
        StoreListSerializer, StoreDetailSerializer,
        DistrictListSerializer, DistrictDetailSerializer,
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
    
