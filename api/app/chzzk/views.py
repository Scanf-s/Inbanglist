from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from common.models import CommonModel
from common.serializers import LiveStreamingModelSerializer



class ChzzkList(generics.ListAPIView):
    queryset = CommonModel.objects.filter(platform='chzzk')
    serializer_class = LiveStreamingModelSerializer
    permission_classes = [IsAuthenticated]

class ChzzkDetail(generics.ListAPIView):
    queryset = CommonModel.objects.filter(platform='chzzk')
    serializer_class = LiveStreamingModelSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        chzzk_streaming_id = request.query_params.get('id')
        if chzzk_streaming_id is not None:
            instance = get_object_or_404(self.queryset, id=chzzk_streaming_id)
            serializer = LiveStreamingModelSerializer(instance=instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
