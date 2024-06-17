from rest_framework.serializers import ModelSerializer
from .models import AfreecaTvModel


class AfreecaTvModelSerializer(ModelSerializer):
    class Meta:
        model = AfreecaTvModel
        fields = '__all__'
