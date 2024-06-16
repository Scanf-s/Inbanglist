from rest_framework.serializers import ModelSerializer
from .models import YoutubeModel

class YouTubeListSerializer(ModelSerializer):

    class Meta:
        model = YoutubeModel
        fields = '__all__'