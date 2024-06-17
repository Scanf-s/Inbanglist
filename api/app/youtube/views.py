from rest_framework import generics
from youtube.models import YoutubeModel
from youtube.serializers import YouTubeModelSerializer

class YoutubeList(generics.ListAPIView):
    queryset = YoutubeModel.objects.all()
    serializer_class = YouTubeModelSerializer

class YoutubeDetail(generics.RetrieveAPIView):
    queryset = YoutubeModel.objects.all()
    serializer_class = YouTubeModelSerializer
