from django.db import models


class CommonModel(models.Model):
    channel_name = models.CharField(max_length=255, null=False, blank=False)  # 스트리머(BJ) 이름
    thumbnail = models.URLField(max_length=1024, null=False, blank=False)  # S3 이미지 링크 저장
    concurrent_viewers = models.PositiveIntegerField(default=0, null=False, blank=False)  # 시청자 수
    title = models.CharField(max_length=255, null=False, blank=False)  # 방송 제목

    class Meta:
        abstract = True
