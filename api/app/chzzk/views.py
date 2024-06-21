from drf_spectacular.utils import extend_schema
from rest_framework import generics

from chzzk.serializers import ChzzkDataSerializer
from common.models import CommonModel


# 참고 링크
# https://www.django-rest-framework.org/api-guide/generic-views/#concrete-view-classes
@extend_schema(tags=["Chzzk"])
class ChzzkListCreateAPI(generics.ListCreateAPIView):
    queryset = CommonModel.objects.filter(platform="chzzk")
    serializer_class = ChzzkDataSerializer


@extend_schema(tags=["Chzzk"])
class ChzzkRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommonModel.objects.filter(platform="chzzk")
    serializer_class = ChzzkDataSerializer
