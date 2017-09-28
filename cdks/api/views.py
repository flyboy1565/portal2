from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView

from cdks.models import Kit, Shipping

from .serializers import KitListSerializer


class KitListAPIView(ListAPIView):
    queryset = Kit.objects.all()
    serializer_class = KitListSerializer