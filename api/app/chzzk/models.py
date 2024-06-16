from django.db import models
from common.models import CommonModel


class ChzzkModel(CommonModel):
    class Meta:
        db_table = 'chzzk'