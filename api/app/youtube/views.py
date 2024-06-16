from rest_framework import generics
from youtube.models import YoutubeModel
from youtube.serializers import YouTubeListSerializer

class YoutubeList(generics.ListAPIView):
    queryset = YoutubeModel.objects.all()
    serializer_class = YouTubeListSerializer
