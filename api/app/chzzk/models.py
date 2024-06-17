from django.db import models
from common.models import CommonModel
from common.platforms import Platforms


class ChzzkModel(CommonModel):
    platform = models.CharField(max_length=50, choices=Platforms.platform_choices, default='chzzk')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'chzzk'
