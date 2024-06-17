from django.db import models
from common.models import CommonModel
from common.platforms import Platforms


class AfreecaTvModel(CommonModel):
    platform = models.CharField(max_length=50, choices=Platforms.platform_choices, default='afreecatv')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'afreecatv'
