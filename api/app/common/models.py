from django.db import models
from django.db.models import CharField, DateTimeField, PositiveIntegerField, TextField, URLField
<<<<<<< HEAD

=======
>>>>>>> 05475956a48e8c6c5d0a2cb9e13625ce4b9b16ec
from common.platforms import Platforms


class CommonModel(models.Model):
    channel_name: CharField = models.CharField(max_length=255, null=False)  # 스트리머(BJ) 이름
    thumbnail: URLField = models.URLField(max_length=1024, null=False)  # S3 이미지 링크 저장
    concurrent_viewers: PositiveIntegerField = models.PositiveIntegerField(default=0, null=False)  # 시청자 수
    title: CharField = models.CharField(max_length=255, null=False)  # 방송 제목
    platform: CharField = models.CharField(
        max_length=50, choices=Platforms.platform_choices, default="youtube", null=False
    )  # 플랫폼
    streaming_link: URLField = models.URLField(max_length=1024, null=False)  # 실시간 방송 링크
    channel_link: URLField = models.URLField(
        max_length=1024, null=False
    )  # 유튜브 : 채널 링크, 치지직 : 프로필 링크, 아프리카TV : 방송국 링크
    channel_description: TextField = models.TextField(null=True)  # 채널(프로필, 방송국)에 써있는 소개글 담는 필드
    followers: PositiveIntegerField = models.PositiveIntegerField(default=0, null=False)  # 구독자, 팔로워, 즐겨찾기 수

    created_at: DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "live_streaming_table"
        verbose_name = "라이브 스트리밍"
        verbose_name_plural = "라이브 스트리밍 목록"

    def __str__(self):
        return f"{self.platform} 에서 방송중인 {self.channel_name}님의 방송제목 {self.title}"
