from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser

from common.models import CommonModel
from youtube.pagination import YoutubePagination
from youtube.serializers import YoutubeDataSerializer

import logging

logger = logging.getLogger(__name__)
# 참고 링크
# https://www.django-rest-framework.org/api-guide/generic-views/#concrete-view-classes


@extend_schema(tags=["Youtube"])
class YoutubeListAPI(generics.ListAPIView):
    queryset = CommonModel.objects.filter(platform="youtube").order_by("-concurrent_viewers")
    serializer_class = YoutubeDataSerializer
    pagination_class = YoutubePagination
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        logger.info("Called YoutubeListAPI")
        response = super().list(request, *args, **kwargs)
        logger.info(f"Response Status Code: {response.status_code}")
        return response


@extend_schema(tags=["Youtube"])
class YoutubeRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommonModel.objects.filter(platform="youtube")
    serializer_class = YoutubeDataSerializer
    permission_classes = [IsAdminUser]
