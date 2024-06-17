from django.db import models

# Create your models here.
class CommonModel(models.Model):
    channel_name = models.CharField(max_length=255) # 스트리머(BJ) 이름
    thumbnail = models.URLField(max_length=1024)  # 나중에 S3에서 이미지 링크를 가져올 예정인데, 어떻게 바꿔야 하나요?
    live_viewer = models.PositiveIntegerField() # viewer는 무조건 양수이므로
    urls = models.URLField(max_length=1024) # 방송 링크
    title = models.CharField(max_length=255) # 방송 제목

    class Meta:
        abstract = True
