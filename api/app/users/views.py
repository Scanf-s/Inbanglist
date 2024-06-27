import os
import requests
from typing import Dict, cast

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from django.shortcuts import redirect
from django.core.exceptions import ImproperlyConfigured
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from common.platforms import OAuthPlatforms
from .models import User, NaverUserId, GoogleUserId
from .serializers import (
    EmptySerializer,
    UserDeleteSerializer,
    UserLoginSerializer,
    UserLogoutSerializer,
    UserRegisterSerializer,
    UserSocialAccountDeleteSerializer,
)
from .tasks import send_activation_email_task
from .utils import confirm_email_token, generate_email_token, get_jwt_tokens_for_user


@extend_schema(tags=["User"])
class UserRegisterAPI(generics.CreateAPIView):
    """
    사용자 회원가입 관련 API
    최초 만든 사용자는 is_active = False로 해두고,
    나중에 메일 인증을 받은 사용자만 is_active = True로 만든다.
    """
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # 비동기로 이메일 전송 작업을 큐에 추가
            # Celery를 사용하여 이메일 전송 작업을 백그라운드에서 비동기적으로 처리
            token = generate_email_token(user.email)  # 사용자 정보가 저장된 후, 이메일 인증 토큰을 생성
            send_activation_email_task.delay(user.email, token)  # 이메일 전송 작업을 비동기로 큐에 추가
            # delay 메서드는 Celery에서 작업을 비동기로 실행하도록 예약하는 메서드 (email send 작업을 비동기로 큐에 추가하고 즉시 반환)
            # 비동기 작업을 큐에 추가한 후, API는 사용자 생성 성공 메시지와 함께 사용자 데이터 및 토큰을 클라이언트에 반환
            return Response(
                {
                    "message": "User created successfully and activation email sent",
                    "user": UserRegisterSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["User"])
class UserLoginAPI(generics.GenericAPIView):
    """
    사용자 로그인 API
    """
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():  # validate email and password in serializer
            user = serializer.validated_data["user"]
            tokens = get_jwt_tokens_for_user(user)
            return Response(
                {
                    "message": "Login successful",
                    "jwt_tokens": tokens,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "message": "Login failed",
                "errors": serializer.errors,
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )


@extend_schema(tags=["User"])
class UserLogoutAPI(generics.GenericAPIView):
    """
    사용자 로그아웃 API 입니다.
    Header에 반드시 Authorization : Bearer {access_token} 넣어주셔야 합니다
    """
    serializer_class = UserLogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                refresh_token_str = serializer.validated_data["refresh_token"]

                # RefreshToken을 블랙리스트에 추가
                try:
                    refresh_token = RefreshToken(refresh_token_str)
                    refresh_token.blacklist()
                except TokenError as e:
                    return Response({"message": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

                return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
            except TokenError as e:
                return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["User"])
class UserDeleteAPI(generics.GenericAPIView):
    """
    사용자 회원 탈퇴 API
    """
    serializer_class = UserDeleteSerializer

    def delete(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                email = serializer.validated_data["email"]
                refresh_token = serializer.validated_data["refresh_token"]
                user = User.objects.get(email=email, oauth_platform__isnull=True)

                # RefreshToken을 블랙리스트에 추가
                try:
                    refresh_token_instance = RefreshToken(refresh_token)
                    refresh_token_instance.blacklist()
                except TokenError as e:
                    return Response({"message": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

                # 사용자 삭제
                user.delete()

                return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            except TokenError:
                return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["User/OAuth2"],
    parameters=[
        OpenApiParameter(
            name='Authorization',
            description='Authorization token',
            required=True,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.HEADER
        ),
        OpenApiParameter(name='email', description='Email of the user', required=True, type=str),
        OpenApiParameter(name='refresh_token', description='Refresh token of the user', required=True, type=str),
        OpenApiParameter(name='oauth_platform', description='OAuth platform (e.g., google, naver)', required=True, type=str)
    ],
)
class UserSocialDeleteAPI(generics.GenericAPIView):
    """
    Social Account 사용자 회원 탈퇴 API
    API 사용 권한을 설정해놓았기 때문에, 로그인한 사용자만 사용할 수 있습니다
    따라서 HTTP Request Header에 반드시 Authorization : Bearer {access_token} 넣어주셔야 합니다.
    """
    serializer_class = UserSocialAccountDeleteSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                email = serializer.validated_data["email"]
                refresh_token = serializer.validated_data["refresh_token"]
                oauth_platform = serializer.validated_data["oauth_platform"]
                user = User.objects.get(email=email, oauth_platform=oauth_platform)

                # RefreshToken을 블랙리스트에 추가
                try:
                    refresh_token_instance = RefreshToken(refresh_token)
                    refresh_token_instance.blacklist()
                except TokenError as e:
                    return Response({"message": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

                # 사용자 삭제
                user.delete()

                return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            except TokenError:
                return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["User"])
class UserEmailActivationAPI(generics.GenericAPIView):
    serializer_class = EmptySerializer

    def get(self, request, token, *args, **kwargs) -> Response:
        email = confirm_email_token(token)
        if email:
            try:
                user = User.objects.filter(email=email).first()
                if user is None:
                    return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
                user.is_active = True
                user.save()  # user's is_active status has changed False to True, save changes into the database
                jwt_token = get_jwt_tokens_for_user(user)

                return Response(
                    {
                        "message": "User created successfully.",
                        "email": user.email,
                        "jwt_tokens": jwt_token,
                    },
                    status=status.HTTP_201_CREATED,
                )
            except:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Invalid or Expired activation code"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["User/OAuth2"])
class UserNaverLoginAPI(generics.GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        response_type = "code"
        naver_client_id = os.getenv("NAVER_CLIENT_ID")
        if not naver_client_id:
            raise ImproperlyConfigured("NAVER_CLIENT_ID is not set")

        main_domain = os.getenv("MAIN_DOMAIN")
        if not main_domain:
            raise ImproperlyConfigured("MAIN_DOMAIN is not set")

        redirect_uri = main_domain + "/api/users/oauth2/naver/callback"

        state = os.getenv("NAVER_CSRF_STATE")
        if not state:
            raise ImproperlyConfigured("NAVER_STATE is not set")

        # Naver Document 에서 확인했던 요청 url
        # https://developers.naver.com/docs/login/api/api.md
        url = "https://nid.naver.com/oauth2.0/authorize"

        # 네이버 로그인 서버로 요청
        return redirect(
            f'{url}?response_type={response_type}&client_id={naver_client_id}&redirect_uri={redirect_uri}&state={state}'
        )


@extend_schema(tags=["User/OAuth2"])
class UserNaverLoginCallBackAPI(generics.GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # https://developers.naver.com/docs/login/api/api.md
        naver_client_id = os.getenv("NAVER_CLIENT_ID")
        naver_client_secret = os.getenv("NAVER_CLIENT_SECRET")
        state = os.getenv("NAVER_CSRF_STATE")

        if not naver_client_id:
            raise ImproperlyConfigured("NAVER_CLIENT_ID is not set")
        if not naver_client_secret:
            raise ImproperlyConfigured("NAVER_CLIENT_SECRET is not set")
        if not state:
            raise ImproperlyConfigured("NAVER_CSRF_STATE is not set")

        authorization_code = request.GET.get("code")
        received_state = request.GET.get("state")

        if not authorization_code:
            return Response({"message": "Authorization code is missing"}, status=status.HTTP_400_BAD_REQUEST)
        if received_state != state:
            return Response({"message": "State value does not match"}, status=status.HTTP_400_BAD_REQUEST)

        token_request_url = "https://nid.naver.com/oauth2.0/token"
        # https://developers.naver.com/docs/login/api/api.md#3-2--%EC%A0%91%EA%B7%BC-%ED%86%A0%ED%81%B0-%EB%B0%9C%EA%B8%89%EA%B0%B1%EC%8B%A0%EC%82%AD%EC%A0%9C-%EC%9A%94%EC%B2%AD
        token_params = {
            "grant_type": "authorization_code",
            "client_id": naver_client_id,
            "client_secret": naver_client_secret,
            "code": authorization_code,
            "state": state,
        }
        token_response = requests.post(token_request_url, data=token_params)
        if token_response.status_code != 200:
            return Response({"message": "Failed to get access token"}, status=status.HTTP_400_BAD_REQUEST)

        token_data = token_response.json()
        access_token = token_data.get("access_token")
        if not access_token:
            return Response({"message": "Failed to get access token"}, status=status.HTTP_400_BAD_REQUEST)

        # url, headers 설정하고, 해당 링크로 사용자 프로필 정보 요청 request
        # https://developers.naver.com/docs/login/profile/profile.md
        user_profile_request_url = "https://openapi.naver.com/v1/nid/me"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        user_response = requests.get(user_profile_request_url, headers=headers)
        if user_response.status_code != 200:
            return Response({"message": "Failed to get user info"}, status=status.HTTP_400_BAD_REQUEST)

        # 네이버 이메일을 가져와야 하는데 왜 다른 이메일이 표시되는건가요?
        # https://developers.naver.com/forum/posts/28835
        user_info = user_response.json()
        user_id = user_info.get("response", {}).get("id")
        user_email = user_info.get("response", {}).get("email")
        if not user_id or not user_email:
            return Response({"message": "Failed to get user info"}, status=status.HTTP_400_BAD_REQUEST)

        # 사용자 존재 여부 확인해서 새로운 사용자를 생성하거나 기존 사용자가 있다면, 로그인
        try:
            user = User.objects.filter(email=user_email, oauth_platform="naver").first()
            if not user:
                # 새로운 소셜계정 사용자라면
                user = User.objects.create_social_user(
                    email=user_email,
                    oauth_platform="naver"
                )
                user.username = user_email.split("@")[0]
                user.is_active = True
                user.save()
            NaverUserId.objects.update_or_create(user=user, defaults={"naver_user_id": user_id}) # 네이버 호출 시 전달받은 user id를 따로 저장
        except Exception as e:
            return Response({"message": "Failed to get or create user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # JWT 토큰 생성
        tokens = get_jwt_tokens_for_user(user)

        return Response(
            {
                "message": "Login successful",
                "jwt_tokens": tokens,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["User/OAuth2"])
class UserGoogleLoginAPI(generics.GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        if not google_client_id:
            raise ImproperlyConfigured("GOOGLE_CLIENT_ID is not set")

        main_domain = os.getenv("MAIN_DOMAIN")
        if not main_domain:
            raise ImproperlyConfigured("MAIN_DOMAIN is not set")

        state = os.getenv("GOOGLE_CSRF_STATE")
        if not state:
            raise ImproperlyConfigured("GOOGLE_CSRF_STATE is not set")

        redirect_uri = f"{main_domain}/api/users/oauth2/google/callback"

        google_auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth"
            "?response_type=code"
            f"&client_id={google_client_id}"
            f"&redirect_uri={redirect_uri}"
            "&scope=openid%20email%20profile"
            f"&state={state}"
        )

        return redirect(google_auth_url)

@extend_schema(tags=["User/OAuth2"])
class UserGoogleLoginCallBackAPI(generics.GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        state = os.getenv("GOOGLE_CSRF_STATE")

        if not google_client_id:
            raise ImproperlyConfigured("GOOGLE_CLIENT_ID is not set")
        if not google_client_secret:
            raise ImproperlyConfigured("GOOGLE_CLIENT_SECRET is not set")
        if not state:
            raise ImproperlyConfigured("GOOGLE_CSRF_STATE is not set")

        authorization_code = request.GET.get("code")
        received_state = request.GET.get("state")

        if not authorization_code:
            return Response({"message": "Authorization code is missing"}, status=status.HTTP_400_BAD_REQUEST)
        if received_state != state:
            return Response({"message": "State value does not match"}, status=status.HTTP_400_BAD_REQUEST)

        token_request_url = "https://oauth2.googleapis.com/token"
        token_params = {
            "grant_type": "authorization_code",
            "client_id": google_client_id,
            "client_secret": google_client_secret,
            "code": authorization_code,
            "redirect_uri": f"{os.getenv('MAIN_DOMAIN')}/api/users/oauth2/google/callback",
        }
        token_response = requests.post(token_request_url, data=token_params)
        if token_response.status_code != 200:
            return Response({"message": "Failed to get access token"}, status=status.HTTP_400_BAD_REQUEST)

        token_data = token_response.json()
        access_token = token_data.get("access_token")
        id_token = token_data.get("id_token")
        if not access_token or not id_token:
            return Response({"message": "Failed to get tokens"}, status=status.HTTP_400_BAD_REQUEST)

        user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}

        user_info_response = requests.get(user_info_url, headers=headers)
        if user_info_response.status_code != 200:
            return Response({"message": "Failed to get user info"}, status=status.HTTP_400_BAD_REQUEST)

        user_info = user_info_response.json()
        user_id = user_info.get("sub")
        user_email = user_info.get("email")
        if not user_email or not user_id:
           return Response({"message": "Failed to get user email and sub(id)"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.filter(email=user_email, oauth_platform="google").first()
            if not user:
                # 새로운 소셜계정 사용자라면
                user = User.objects.create_social_user(
                    email=user_email,
                    oauth_platform="google"
                )
                user.username = user_email.split("@")[0]
                user.is_active = True
                user.save()
            GoogleUserId.objects.update_or_create(user=user, defaults={"google_user_id": user_id})
            # Google 호출 시 전달받은 sub를 user_id 로 사용하여 따로 저장
        except Exception as e:
            return Response({"message": "Failed to get or create user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # JWT 토큰 생성
        tokens = get_jwt_tokens_for_user(user)

        return Response(
            {
                "message": "Login successful",
                "jwt_tokens": tokens,
            },
            status=status.HTTP_200_OK,
        )
