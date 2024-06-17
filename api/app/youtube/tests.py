from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from youtube.models import YoutubeModel, YoutubeStreamDetails


class YoutubeAPITest(APITestCase):
    def setUp(self):
        self.youtube_model = YoutubeModel.objects.create(
            channel_name="냥집사",
            thumbnail="https://www.example.com/thumbnail.jpg",
            concurrent_viewers=1000,
            title="LIVE - 냥냥펀치와 꾹꾹이 직관",
        )

        self.youtube_details = YoutubeStreamDetails.objects.create(
            description="냥집사의 하루중 가장 중요한 업무! 냥이의 행복을 지켜라",
            streaming_link="https://www.youtube.com/watch?v=abcd1234",
            channel_descript="냥집사의 집사업무 꿀팁전수 채널",
            youtube_model=self.youtube_model
        )

    # api/v1/youtube [GET]
    def test_get_youtube_list(self):
        url = reverse('youtube_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['channel_name'], "냥집사")
        self.assertEqual(response.data[0]['concurrent_viewers'], 1000)
        self.assertEqual(response.data[0]['details']['description'], "냥집사의 하루중 가장 중요한 업무! 냥이의 행복을 지켜라")
        self.assertEqual(response.data[0]['details']['streaming_link'], "https://www.youtube.com/watch?v=abcd1234")
        self.assertEqual(response.data[0]['details']['channel_descript'], "냥집사의 집사업무 꿀팁전수 채널")

    # api/v1/youtube/{pk} [GET]
    def test_get_youtube_detail(self):
        url=reverse('youtube_detail', args=[self.youtube_model.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['channel_name'], "냥집사")
        self.assertEqual(response.data['concurrent_viewers'], 1000)
        self.assertEqual(response.data['details']['description'], "냥집사의 하루중 가장 중요한 업무! 냥이의 행복을 지켜라")
        self.assertEqual(response.data['details']['streaming_link'], "https://www.youtube.com/watch?v=abcd1234")
        self.assertEqual(response.data['details']['channel_descript'], "냥집사의 집사업무 꿀팁전수 채널")

    # 데이터가 없는 경우 테스트
    def test_get_empty_youtube_list(self):
        YoutubeModel.objects.all().delete()
        url = reverse('youtube_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    # 잘못된 URL 테스트
    def test_get_invalid_url(self):
        url = "/api/v1/invalid/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
