from rest_framework.serializers import ModelSerializer
from .models import YoutubeModel, YoutubeStreamDetails


class YoutubeStreamDetailsSerializer(ModelSerializer):
    class Meta:
        model = YoutubeStreamDetails
        fields = '__all__'


class YouTubeModelSerializer(ModelSerializer):
    details = YoutubeStreamDetailsSerializer()
    class Meta:
        model = YoutubeModel
        fields = '__all__'