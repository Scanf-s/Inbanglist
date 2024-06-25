from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User
from .serializers import UserDeleteSerializer, UserLoginSerializer, UserLogoutSerializer, UserRegisterSerializer, EmptySerializer
from .utils import confirm_email_token


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
    최초 만든 사용자는 is_active = False로 해두고,
    나중에 메일 인증을 받은 사용자만 is_active = True로 만든다.
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
                # AccessToken 제거
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


@extend_schema(tags=["User"])
class UserEmailActivationAPI(generics.GenericAPIView):

    serializer_class = EmptySerializer

    def get(self, request, token, *args, **kwargs) -> Response:
        email = confirm_email_token(token)
        if email:
            try:
                user = User.objects.filter(email=email).first()
                if user is None:
                    return Response(
                        {"message": "User not found"},
                        status=status.HTTP_404_NOT_FOUND
                    )
                user.is_active = True
                user.save()
                return Response(
                    {
                        "message": "User created successfully. Please check your email to activate your account.",
                    },
                    status=status.HTTP_201_CREATED,
                )
            except:
                return Response(
                    {"message": "User not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response({"message": "Invalid or Expired activation code"}, status=status.HTTP_400_BAD_REQUEST)
