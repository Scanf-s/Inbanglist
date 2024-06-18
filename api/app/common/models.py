from django.db import models
from common.platforms import Platforms


class CommonModel(models.Model):
    channel_name = models.CharField(max_length=255, null=False, blank=False)  # 스트리머(BJ) 이름
    thumbnail = models.URLField(max_length=1024, null=False, blank=False)  # S3 이미지 링크 저장
    concurrent_viewers = models.PositiveIntegerField(default=0, null=False, blank=False)  # 시청자 수
    title = models.CharField(max_length=255, null=False, blank=False)  # 방송 제목
    platform = models.CharField(max_length=50, choices=Platforms.platform_choices, default='youtube', null=False, blank=False) # 플랫폼
    streaming_link = models.URLField(max_length=1024, null=False, blank=False) # 실시간 방송 링크
    channel_link = models.URLField(max_length=1024, null=False, blank=False) # 유튜브 : 채널 링크, 치지직 : 프로필 링크, 아프리카TV : 방송국 링크
    channel_description = models.TextField(null=True, blank=True) # 채널(프로필, 방송국)에 써있는 소개글 담는 필드
    followers = models.PositiveIntegerField(default=0, null=False, blank=False) # 구독자, 팔로워, 즐겨찾기 수

    class Meta:
        db_table = 'live_streaming_table'
        verbose_name = "라이브 스트리밍"
        verbose_name_plural = "라이브 스트리밍 목록"

    def __str__(self):
        return f"{self.platform} 에서 방송중인 {self.channel_name}님의 방송제목 {self.title}"
