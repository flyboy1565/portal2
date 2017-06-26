from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView

from phones.models import *

from .serializers import PhoneBillingDetailSerializer, PhoneBillingListSerializer


class PhoneBillingDetailAPIView(RetrieveAPIView):
    queryset = PhoneBilling.objects.all()
    serializer_class = PhoneBillingDetailSerializer
    lookup_field = 'store'


class PhoneBillingListAPIView(ListAPIView):
    queryset = PhoneBilling.objects.all()
    serializer_class = PhoneBillingListSerializer