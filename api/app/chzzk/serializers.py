from rest_framework.serializers import ModelSerializer
from .models import ChzzkModel


class ChzzkModelSerializer(ModelSerializer):
    class Meta:
        model = ChzzkModel
        fields = '__all__'