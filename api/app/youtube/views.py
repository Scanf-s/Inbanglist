from typing import Optional

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from common.models import CommonModel
from common.serializers import LiveStreamingModelSerializer


class YoutubeListAPI(viewsets.ViewSet):
    """
    기본적인 Youtube 스트리밍 리스트 API
    """

    queryset: QuerySet = CommonModel.objects.filter(platform="youtube")

<<<<<<< HEAD
=======

>>>>>>> 05475956a48e8c6c5d0a2cb9e13625ce4b9b16ec
    @extend_schema(
        responses={200: LiveStreamingModelSerializer(many=True)},
    )
    def list(self, request) -> Response:
        serializer: LiveStreamingModelSerializer = LiveStreamingModelSerializer(
            self.queryset,
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: LiveStreamingModelSerializer},
    )
    def retrieve(self, request, pk: Optional[int] = None) -> Response:
        instance: CommonModel = get_object_or_404(self.queryset, id=pk)
        serializer: LiveStreamingModelSerializer = LiveStreamingModelSerializer(instance=instance)
<<<<<<< HEAD
=======

>>>>>>> 05475956a48e8c6c5d0a2cb9e13625ce4b9b16ec
        return Response(serializer.data, status=status.HTTP_200_OK)
