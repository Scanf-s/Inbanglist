from django.db import models
from common.models import CommonModel
# Create your models here.
class YoutubeModel(CommonModel):
    class Meta:
        db_table = 'youtube'