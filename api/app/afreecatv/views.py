from rest_framework import generics
from afreecatv.models import AfreecaTvModel
from afreecatv.serializers import AfreecaTvModelSerializer

class AfreecaTvList(generics.ListAPIView):
    queryset = AfreecaTvModel.objects.all()
    serializer_class = AfreecaTvModelSerializer

class AfreecaTvDetail(generics.RetrieveAPIView):
    queryset = AfreecaTvModel.objects.all()
    serializer_class = AfreecaTvModelSerializer
