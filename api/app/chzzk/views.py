from rest_framework import generics
from chzzk.models import ChzzkModel
from chzzk.serializers import ChzzkModelSerializer

class ChzzkList(generics.ListAPIView):
    queryset = ChzzkModel.objects.all()
    serializer_class = ChzzkModelSerializer

class ChzzkDetail(generics.RetrieveAPIView):
    queryset = ChzzkModel.objects.all()
    serializer_class = ChzzkModelSerializer
