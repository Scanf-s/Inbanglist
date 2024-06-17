from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from chzzk.models import ChzzkModel
from chzzk.serializers import ChzzkModelSerializer

class ChzzkList(generics.ListAPIView):
    queryset = ChzzkModel.objects.all()
    serializer_class = ChzzkModelSerializer
    permission_classes = [IsAuthenticated]

class ChzzkDetail(generics.RetrieveAPIView):
    queryset = ChzzkModel.objects.all()
    serializer_class = ChzzkModelSerializer
    permission_classes = [IsAuthenticated]
