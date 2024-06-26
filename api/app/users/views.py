from typing import cast

from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User
from .serializers import (
    EmptySerializer,
    UserDeleteSerializer,
    UserLoginSerializer,
    UserLogoutSerializer,
    UserRegisterSerializer,
)
from .tasks import send_activation_email_task
from .utils import confirm_email_token, generate_email_token

from typing import Dict


def get_tokens_for_user(user: User) -> Dict[str, str]:
    refresh: RefreshToken = cast(RefreshToken, RefreshToken.for_user(user))
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


@extend_schema(tags=["User"])
class UserRegisterAPI(generics.CreateAPIView):
    """
    사용자 회원가입 관련 API
    최초 만든 사용자는 is_active = False로 해두고,
    나중에 메일 인증을 받은 사용자만 is_active = True로 만든다.
    """

    serializer_class = UserRegisterSerializer

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
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():  # validate email and password in serializer
            user = serializer.validated_data["user"]
            tokens = get_tokens_for_user(user)
            return Response(
                {
                    "message": "Login successful",
                    "user": UserLoginSerializer(user).data,
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
    serializer_class = UserLogoutSerializer

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
                refresh_token = RefreshToken(serializer.validated_data["refresh_token"])
                refresh_token.blacklist()

                user = User.objects.get(email=serializer.validated_data["email"])
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
                jwt_token = get_tokens_for_user(user)

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
