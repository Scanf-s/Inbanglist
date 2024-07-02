import os

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User


class UserTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("user_register")
        self.login_url = reverse("user_login")
        self.logout_url = reverse("user_logout")
        self.delete_url = reverse("user_delete")
        self.userinfo_url = reverse("user_info")
        self.social_login_url = reverse("user_oauth2_google_login")

        self.user_data = {
            "username": "testuser",
            "email": "djangotestuser0000@example.com",
            "password": "securepassword123",
        }

        self.social_user_data = {
            "email": "socialuser@example.com",
            "oauth_platform": "google",
            "oauth2_user_id": "123456789",
        }

    def test_user_registration(self):
        # Given: 사용자 등록 데이터 준비
        # When: 사용자 등록 요청을 보냄
        response = self.client.post(self.register_url, self.user_data, format="json")

        # Then: 응답이 201 CREATED 이어야 함
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=self.user_data["email"]).exists())

    def test_user_login(self):
        # Given: 사용자 등록 및 활성화
        self.client.post(self.register_url, self.user_data, format="json")

        user = User.objects.get(email=self.user_data["email"])
        user.is_active = True
        user.save()

        login_data = {"email": self.user_data["email"], "password": self.user_data["password"]}

        # When: 로그인 요청을 보냄
        response = self.client.post(self.login_url, login_data, format="json")

        # Then: 응답이 200 OK 이어야 하고, JWT 토큰이 포함되어 있어야 함
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("jwt_tokens", response.data)

    def test_user_logout(self):
        # Given: 사용자 등록, 활성화 및 로그인
        self.client.post(self.register_url, self.user_data, format="json")

        user = User.objects.get(email=self.user_data["email"])
        user.is_active = True
        user.save()

        login_data = {"email": self.user_data["email"], "password": self.user_data["password"]}
        login_response = self.client.post(self.login_url, login_data, format="json")
        refresh_token = login_response.data["jwt_tokens"]["refresh"]
        logout_data = {"refresh_token": refresh_token}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['jwt_tokens']['access']}")

        # When: 로그아웃 요청을 보냄
        response = self.client.post(self.logout_url, logout_data, format="json")

        # Then: 응답이 200 OK 이어야 함
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_delete(self):
        """
        A test case to simulate a user deletion process:

        - Given: A user is registered, activated, and logged in.
        - When: A request to delete the user is sent.
        - Then: The response status should be 200 OK, and the user should no longer exist.
        """
        # Given: 사용자 등록, 활성화 및 로그인
        self.client.post(self.register_url, self.user_data, format="json")
        user = User.objects.get(email=self.user_data["email"])
        user.is_active = True
        user.save()
        login_data = {"email": self.user_data["email"], "password": self.user_data["password"]}
        login_response = self.client.post(self.login_url, login_data, format="json")
        refresh_token = login_response.data["jwt_tokens"]["refresh"]
        delete_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
            "refresh_token": refresh_token,
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['jwt_tokens']['access']}")

        # When: 사용자 삭제 요청을 보냄
        response = self.client.delete(self.delete_url, delete_data, format="json")

        # Then: 응답이 200 OK 이어야 하고, 사용자가 존재하지 않아야 함
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(User.objects.filter(email=self.user_data["email"]).exists())

    def test_user_info(self):
        """
        A test case to simulate a user information retrieval process:

        - Given: A user is registered, activated, and logged in.
        - When: A request to retrieve the user information is sent.
        - Then: The response status should be 200 OK, and the user information should be returned.
        """
        # Given: 사용자 등록, 활성화 및 로그인
        self.client.post(self.register_url, self.user_data, format="json")
        user = User.objects.get(email=self.user_data["email"])
        user.is_active = True
        user.save()
        login_data = {"email": self.user_data["email"], "password": self.user_data["password"]}
        login_response = self.client.post(self.login_url, login_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['jwt_tokens']['access']}")

        # When: 사용자 정보 조회 요청
        response = self.client.get(self.userinfo_url, format="json")

        # Then: 응답이 200 OK 이어야 하며, 사용자 정보가 포함되어 있어야 함
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["email"], self.user_data["email"])
        self.assertEqual(response.data["user"]["username"], self.user_data["username"])
        self.assertEqual(response.data["user"]["profile_image"], os.getenv("DEFAULT_PROFILE_IMAGE"))
        self.assertEqual(response.data["user"]["is_staff"], False)
