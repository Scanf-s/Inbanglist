from common.models import CommonModel
from common.serializers import LiveStreamingModelSerializer


class ChzzkDataSerializer(LiveStreamingModelSerializer):
    class Meta:
        model = CommonModel
        fields = "__all__"
