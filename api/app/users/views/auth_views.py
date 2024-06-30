import logging
import os
from typing import Union

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils import timezone
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from users.models import User
from users.serializers import (
    EmptySerializer,
    UserDeleteSerializer,
    UserInfoSerializer,
    UserLoginSerializer,
    UserLogoutSerializer,
    UserRegisterSerializer,
)
from users.tasks import send_activation_email_task
from users.utils import confirm_email_token, generate_email_token, get_jwt_tokens_for_user

logger = logging.getLogger(__name__)


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
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()  # is_valid()=True 인 경우만 데이터베이스에 사용자 추가
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
            user.last_login = timezone.now()
            user.save()
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


@extend_schema(
    tags=["User"],
    parameters=[
        OpenApiParameter(
            name="Authorization",
            description="Authorization token",
            required=True,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.HEADER,
        ),
        OpenApiParameter(name="email", description="Email of the user", required=True, type=str),
        OpenApiParameter(name="password", description="Password of the user", required=True, type=str),
        OpenApiParameter(name="refresh_token", description="Refresh token of the user", required=True, type=str),
    ],
)
class UserDeleteAPI(generics.GenericAPIView):
    """
    사용자 회원 탈퇴 API
    소셜 사용자 회원 탈퇴는 User/OAuth2를 참고해 주세요
    """

    serializer_class = UserDeleteSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def delete(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                email = serializer.validated_data["email"]
                refresh_token = serializer.validated_data["refresh_token"]
                user = User.objects.get(email=email, oauth_platform="none")

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
class UserInfoAPI(generics.RetrieveAPIView):
    serializer_class = UserInfoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [
        JWTAuthentication
    ]  # JWTAuthentication가 요청 헤더에서 access_token을 자동으로 추출하고 유효성 검사

    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(
            data={
                "message": "User data fetched successfully",
                "user": {
                    "username": serializer.data["username"],
                    "email": serializer.data["email"],
                    "user_profile_image": "https://www.example.com",  # serializer.data.get("profile_image", None),
                    "oauth_platform": serializer.data.get("oauth_platform", None),
                },
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["User"])
class UserEmailActivationAPI(generics.GenericAPIView):
    """
    사용자 이메일 인증링크를 처리하는 API
    """

    serializer_class = EmptySerializer
    permission_classes = [AllowAny]

    def get(self, request, token, *args, **kwargs) -> Union[Response, HttpResponseRedirect]:
        email = confirm_email_token(token)
        if email:
            try:
                user = User.objects.filter(email=email).first()
                if user is None:
                    return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
                user.is_active = True
                user.save()  # user's is_active status has changed False to True, save changes into the database
                return redirect(f"{os.getenv('MAIN_DOMAIN')}/activate/{token}")
            except:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Invalid or Expired activation code"}, status=status.HTTP_400_BAD_REQUEST)
