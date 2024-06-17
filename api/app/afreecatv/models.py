from django.db import models
from common.models import CommonModel


class AfreecaTvModel(CommonModel):
    class Meta:
        db_table = 'afreecatv'