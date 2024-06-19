from rest_framework.serializers import ModelSerializer

from common.models import CommonModel


class LiveStreamingModelSerializer(ModelSerializer):
    class Meta:
        model = CommonModel
        fields = "__all__"
