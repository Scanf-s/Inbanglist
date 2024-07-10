from celery import shared_task
from django.core.cache import cache

from common.models import CommonModel


@shared_task
def load_data_to_cache():
    # RDS에서 데이터 로드
    data = list(CommonModel.objects.all().order_by("-concurrent_viewers"))

    # 캐시에 데이터 저장 (10분 TTL)
    cache.set("external_data", data, timeout=600)
    print("Data loaded to cache successfully")
