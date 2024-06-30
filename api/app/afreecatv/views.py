import logging

from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser

from afreecatv.pagination import AfreecaTVPagination
from afreecatv.serializers import AfreecaTvDataSerializer
from common.models import CommonModel

# 참고 링크
# https://www.django-rest-framework.org/api-guide/generic-views/#concrete-view-classes

logger = logging.getLogger(__name__)


@extend_schema(tags=["AfreecaTV"])
class AfreecaTvListAPI(generics.ListAPIView):
    queryset = CommonModel.objects.filter(platform="afreecatv").order_by("-concurrent_viewers")
    serializer_class = AfreecaTvDataSerializer
    pagination_class = AfreecaTVPagination
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        logger.info("GET /api/v1/afreecatv")
        response = super().list(request, *args, **kwargs)
        logger.info(f"Response Status Code: {response.status_code}")
        return response


@extend_schema(tags=["AfreecaTV"])
class AfreecaTvRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommonModel.objects.filter(platform="afreecatv")
    serializer_class = AfreecaTvDataSerializer
    permission_classes = [IsAdminUser]
