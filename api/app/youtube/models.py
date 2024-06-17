from django.db import models

from common.models import CommonModel
from common.platforms import Platforms


class YoutubeStreamDetails(models.Model):
    description = models.TextField(null=True, blank=True)  # 방송 세부 설명
    streaming_link = models.URLField(max_length=1024, null=False, blank=False)  # 방송 링크
    channel_descript = models.TextField(null=True, blank=True)  # 유튜브 채널 설명
    youtube_model = models.OneToOneField(to='youtube.YoutubeModel', on_delete=models.CASCADE, related_name='details', null=True, blank=True)

    def __str__(self):
        return self.description[:50]


class YoutubeModel(CommonModel):
    platform = models.CharField(max_length=50, choices=Platforms.platform_choices, default='youtube')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'youtube'
