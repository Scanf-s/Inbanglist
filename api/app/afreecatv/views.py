from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from afreecatv.models import AfreecaTvModel
from afreecatv.serializers import AfreecaTvModelSerializer

class AfreecaTvList(generics.ListAPIView):
    queryset = AfreecaTvModel.objects.all()
    serializer_class = AfreecaTvModelSerializer
    permission_classes = [IsAuthenticated]

class AfreecaTvDetail(generics.RetrieveAPIView):
    queryset = AfreecaTvModel.objects.all()
    serializer_class = AfreecaTvModelSerializer
    permission_classes = [IsAuthenticated]
