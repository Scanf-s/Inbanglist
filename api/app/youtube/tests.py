from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from youtube.models import YoutubeModel

from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile # 파일 관련 테스트할때 사용

class YoutubeAPITest(APITestCase):
    pass
