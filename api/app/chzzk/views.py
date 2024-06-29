from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser

from chzzk.pagination import ChzzkPagination
from chzzk.serializers import ChzzkDataSerializer
from common.models import CommonModel

import logging

logger = logging.getLogger(__name__)

# 참고 링크
# https://www.django-rest-framework.org/api-guide/generic-views/#concrete-view-classes
@extend_schema(tags=["Chzzk"])
class ChzzkListAPI(generics.ListAPIView):
    queryset = CommonModel.objects.filter(platform="chzzk").order_by("-concurrent_viewers")
    serializer_class = ChzzkDataSerializer
    pagination_class = ChzzkPagination
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        logger.info("Called ChzzkListAPI")
        response = super().list(request, *args, **kwargs)
        logger.info(f"Response Status Code: {response.status_code}")
        return response

@extend_schema(tags=["Chzzk"])
class ChzzkRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommonModel.objects.filter(platform="chzzk")
    serializer_class = ChzzkDataSerializer
    permission_classes = [IsAdminUser]
