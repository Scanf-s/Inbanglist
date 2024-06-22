"""
AfreecaTV, Chzzk, Youtube와 다르게 API를 구현한 이유

AfreecaTv, Chzzk, Youtube는 단순한 CRUD API만 작성해주면 되기 때문에
https://www.django-rest-framework.org/api-guide/generic-views/#concrete-view-classes
해당 링크에 있는 Concrete View Class를 사용해서 간단하게 구현할 수 있습니다.

하지만 User API의 경우, 아직 해당 내용에 대한 조사가 부족하기도 했고,
미리 구현된 Concrete View Class를 사용하면 제가 원하는 동작을 만들기가 어렵습니다.
따라서 그냥 CreateAPIView, GenericAPIView를 사용해서 메소드를 오버라이딩하여 원하는대로 동작하도록 구현했습니다.
"""

from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User
from .serializers import UserDeleteSerializer, UserLoginSerializer, UserLogoutSerializer, UserRegisterSerializer


def get_tokens_for_user(user: User):
    refresh: RefreshToken = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@extend_schema(tags=["User"])
class UserRegisterAPI(generics.CreateAPIView):
    """
    사용자 회원가입 관련 API
    """

    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response(
                {
                    "message": "User created successfully",
                    "user": UserRegisterSerializer(user).data,
                    "tokens": tokens,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["User"])
class UserLoginAPI(generics.GenericAPIView):
    """
    사용자 로그인 관련 API
    """

    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(email=serializer.validated_data["email"]).first()
            if user and user.check_password(serializer.validated_data["password"]):
                tokens = get_tokens_for_user(user)
                return Response(
                    {
                        "message": "Login successful",
                        "user": UserLoginSerializer(user).data,
                        "tokens": tokens,
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
    사용자 로그아웃 API
    """

    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                token = RefreshToken(serializer.validated_data["refresh"])
                token.blacklist()
                return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
            except TokenError:
                return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["User"])
class UserDeleteAPI(generics.GenericAPIView):
    """
    사용자 회원 탈퇴 API
    """

    serializer_class = UserDeleteSerializer

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                token = RefreshToken(serializer.validated_data["refresh"])
                token.blacklist()
                user = User.objects.get(email=serializer.validated_data["email"])
                user.delete()
                return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            except TokenError:
                return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
