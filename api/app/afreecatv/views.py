from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser

from afreecatv.pagination import AfreecaTVPagination
from afreecatv.serializers import AfreecaTvDataSerializer
from common.models import CommonModel

# 참고 링크
# https://www.django-rest-framework.org/api-guide/generic-views/#concrete-view-classes


@extend_schema(tags=["AfreecaTV"])
class AfreecaTvListAPI(generics.ListAPIView):
    queryset = CommonModel.objects.filter(platform="afreecatv").order_by("-concurrent_viewers")
    serializer_class = AfreecaTvDataSerializer
    pagination_class = AfreecaTVPagination
    permission_classes = [AllowAny]


@extend_schema(tags=["AfreecaTV"])
class AfreecaTvRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommonModel.objects.filter(platform="afreecatv")
    serializer_class = AfreecaTvDataSerializer
    permission_classes = [IsAdminUser]
