from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView

from devices.models import System, SystemIP, DownHistory

from .serializers import SystemListSerializer


class SystemListAPIView(ListAPIView):
    queryset = System.objects.all()
    serializer_class = SystemListSerializer