from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from youtube.models import YoutubeModel
from youtube.serializers import YouTubeModelSerializer



class YoutubeList(generics.ListAPIView):
    queryset = YoutubeModel.objects.all()
    serializer_class = YouTubeModelSerializer
    permission_classes = [IsAuthenticated]

class YoutubeDetail(generics.ListAPIView):
    queryset = YoutubeModel.objects.all()
    serializer_class = YouTubeModelSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        youtube_streaming_id = request.query_params.get('id')
        if youtube_streaming_id is not None:
            try:
                data = YoutubeModel.objects.get(id=youtube_streaming_id)
                serializer = YouTubeModelSerializer(instance=data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except YoutubeModel.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)
