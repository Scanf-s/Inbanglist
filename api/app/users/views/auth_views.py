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


@extend_schema(
    tags=["User"],
    summary="Register a new user",
    description="""
        This API endpoint allows a new user to register.
        The registered user will initially have `is_active=False` and
        will only be activated after email verification.

        ## Key Features:
        - **Registration**: Creates a new user with the provided username, email, and password.
        - **Email Verification**: Sends an email verification link to the registered email.

        ## Parameters:
        - **username**: The nickname of the user (required).
        - **email**: The email address of the user (required).
        - **password**: The password of the user (required).

        ## Response:
        - **201 Created**: User created successfully and activation email sent.
        - **400 Bad Request**: Invalid data or user already exists.

        ## Example:
        ### Request:
        ```
        POST /api/v1/users/register/
        {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword123"
        }
        ```

        ### Response:
        ```
        {
            "message": "User created successfully and activation email sent"
        }
        ```
    """,
    parameters=[
        OpenApiParameter(name="username", description="nickname of the user", required=True, type=OpenApiTypes.STR),
        OpenApiParameter(name="email", description="Email of the user", required=True, type=OpenApiTypes.STR),
        OpenApiParameter(name="password", description="Password of the user", required=True, type=OpenApiTypes.STR),
    ],
)
class UserRegisterAPI(generics.CreateAPIView):
    """
    API endpoint for user registration.
    Initially, the created user will have is_active=False,
    and will be activated only after email verification.
    """

    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs) -> Response:
        logger.info("POST /api/v1/users/register")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()  # is_valid()=True 인 경우만 데이터베이스에 사용자 추가
            # 비동기로 이메일 전송 작업을 큐에 추가
            # Celery를 사용하여 이메일 전송 작업을 백그라운드에서 비동기적으로 처리
            token = generate_email_token(user.email)  # 사용자 정보가 저장된 후, 이메일 인증 토큰을 생성
            send_activation_email_task.delay(user.email, token)  # 이메일 전송 작업을 비동기로 큐에 추가
            # delay 메서드는 Celery에서 작업을 비동기로 실행하도록 예약하는 메서드 (email send 작업을 비동기로 큐에 추가하고 즉시 반환)
            # 비동기 작업을 큐에 추가한 후, API는 사용자 생성 성공 메시지와 함께 사용자 데이터 및 토큰을 클라이언트에 반환
            logger.info(f"User {user.email} created and activation email sent.")
            return Response(
                {
                    "message": "User created successfully and activation email sent",
                },
                status=status.HTTP_201_CREATED,
            )
        logger.error(f"User registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["User"],
    summary="User login API",
    description="""
        This API endpoint allows a user to log in using their email and password.

        ## Key Features:
        - **Authentication**: Validates the user's email and password.
        - **JWT Token Generation**: Generates JWT tokens (access and refresh) upon successful login.

        ## Parameters:
        - **email**: The email address of the user (required).
        - **password**: The password of the user (required).

        ## Response:
        - **200 OK**: Login successful and JWT tokens returned.
        - **401 Unauthorized**: Login failed due to invalid credentials.

        ## Example:
        ### Request:
        ```
        POST /api/v1/users/login/
        {
            "email": "user@example.com",
            "password": "securepassword123"
        }
        ```

        ### Response (success):
        ```
        {
            "message": "Login successful",
            "jwt_tokens": {
                "access": "access_token",
                "refresh": "refresh_token"
            }
        }
        ```

        ### Response (failure):
        ```
        {
            "message": "Login failed",
            "errors": {
                "email": ["This field is required."],
                "password": ["This field is required."]
            }
        }
        ```
    """,
    parameters=[
        OpenApiParameter(name="email", description="Email of the user", required=True, type=OpenApiTypes.STR),
        OpenApiParameter(name="password", description="Password of the user", required=True, type=OpenApiTypes.STR),
    ],
)
class UserLoginAPI(generics.GenericAPIView):
    """
    API endpoint for user login.
    Validates email and password and returns JWT tokens if successful.
    """

    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs) -> Response:
        logger.info("POST /api/v1/users/login")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():  # validate email and password in serializer
            user = serializer.validated_data["user"]
            user.last_login = timezone.now()
            user.save()
            tokens = get_jwt_tokens_for_user(user)

            logger.info(f"User {user.email} logged in successfully.")
            return Response(
                {
                    "message": "Login successful",
                    "jwt_tokens": tokens,
                },
                status=status.HTTP_200_OK,
            )

        logger.error(f"User login failed: {serializer.errors}")
        return Response(
            {
                "message": "Login failed",
                "errors": serializer.errors,
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )


@extend_schema(
    tags=["User"],
    summary="User logout API",
    description="""
        This API endpoint allows a user to log out by blacklisting their refresh token.

        ## Key Features:
        - **Token Blacklisting**: Adds the refresh token to the blacklist to invalidate it.

        ## Parameters:
        - **Authorization**: The access token of the user (required, in header).
        - **refresh_token**: The refresh token of the user (required).

        ## Response:
        - **200 OK**: Logout successful.
        - **400 Bad Request**: Invalid token or other errors.

        ## Example:
        ### Request:
        ```
        POST /api/v1/users/logout/
        Headers: {
            "Authorization": "Bearer access_token"
        }
        {
            "refresh_token": "refresh_token_string"
        }
        ```

        ### Response (success):
        ```
        {
            "message": "Logout successful"
        }
        ```

        ### Response (failure):
        ```
        {
            "message": "Invalid refresh token"
        }
        ```
    """,
    parameters=[
        OpenApiParameter(
            name="Authorization",
            description="Authorization access token",
            required=True,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.HEADER,
        ),
        OpenApiParameter(name="refresh_token", description="Refresh token of the user", required=True,
                         type=OpenApiTypes.STR),
    ],
)
class UserLogoutAPI(generics.GenericAPIView):
    """
    API endpoint for user logout.
    Blacklists the refresh token to invalidate it.
    """

    serializer_class = UserLogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs) -> Response:
        logger.info("POST /api/v1/users/logout")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                refresh_token_str = serializer.validated_data["refresh_token"]

                # RefreshToken을 블랙리스트에 추가
                try:
                    refresh_token = RefreshToken(refresh_token_str)
                    refresh_token.blacklist()
                except TokenError as e:
                    logger.error(f"Invalid refresh token: {str(e)}")
                    return Response({"message": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

                logger.info(f"User {request.user.email} logged out successfully.")
                return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
            except TokenError as e:
                logger.error(f"Token error: {str(e)}")
                return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        logger.error(f"Logout failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["User"],
    summary="User account deletion API",
    description="""
        This API endpoint allows a user to delete their account.

        ## Key Features:
        - **Email Verification**: Ensures the email belongs to the user who is requesting the deletion.
        - **Token Blacklisting**: Adds the refresh token to the blacklist to invalidate it.

        ## Parameters:
        - **Authorization**: The access token of the user (required, in header).
        - **email**: The email address of the user (required).
        - **password**: The password of the user (required).
        - **refresh_token**: The refresh token of the user (required).

        ## Response:
        - **200 OK**: User deleted successfully.
        - **400 Bad Request**: Invalid token or other errors.
        - **404 Not Found**: User not found.

        ## Example:
        ### Request:
        ```
        DELETE /api/v1/users/delete/
        Headers: {
            "Authorization": "Bearer access_token"
        }
        {
            "email": "user@example.com",
            "password": "userpassword",
            "refresh_token": "refresh_token_string"
        }
        ```

        ### Response (success):
        ```
        {
            "message": "User deleted successfully"
        }
        ```

        ### Response (failure):
        ```
        {
            "message": "Invalid refresh token"
        }
        ```
    """,
    parameters=[
        OpenApiParameter(
            name="Authorization",
            description="Authorization access token",
            required=True,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.HEADER,
        ),
        OpenApiParameter(name="email", description="Email of the user", required=True, type=OpenApiTypes.STR),
        OpenApiParameter(name="password", description="Password of the user", required=True, type=OpenApiTypes.STR),
        OpenApiParameter(name="refresh_token", description="Refresh token of the user", required=True,
                         type=OpenApiTypes.STR),
    ],
)
class UserDeleteAPI(generics.GenericAPIView):
    """
    API endpoint for user account deletion.
    Only non-social users can delete their accounts via this endpoint.
    For social user account deletion, refer to the User/OAuth2 API.
    """

    serializer_class = UserDeleteSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def delete(self, request, *args, **kwargs) -> Response:
        logger.info("DELETE /api/v1/users/delete")
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
                    logger.error(f"Invalid refresh token: {str(e)}")
                    return Response({"message": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

                # 사용자 삭제
                user.delete()
                logger.info(f"User {email} deleted successfully.")
                return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                logger.error(f"User not found: {email}")
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            except TokenError as e:
                logger.error(f"Token error: {str(e)}")
                return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        logger.error(f"User deletion failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["User"],
    summary="User information retrieval API",
    description="""
        This API endpoint allows a user to retrieve their account information.

        ## Key Features:
        - **Authentication**: Requires a valid JWT access token.
        - **User Information**: Returns user information including username, email, profile image, staff status, and OAuth platform.

        ## Parameters:
        - **Authorization**: The access token of the user (required, in header).

        ## Response:
        - **200 OK**: User data fetched successfully.
        - **401 Unauthorized**: Invalid or missing access token.

        ## Example:
        ### Request:
        ```
        GET /api/v1/users/info/
        Headers: {
            "Authorization": "Bearer access_token"
        }
        ```

        ### Response (success):
        ```
        {
            "message": "User data fetched successfully",
            "user": {
                "username": "user",
                "email": "user@example.com",
                "profile_image": "http://example.com/image.jpg",
                "is_staff": false,
                "oauth_platform": "none"
            }
        }
        ```

        ### Response (failure):
        ```
        {
            "detail": "Authentication credentials were not provided."
        }
        ```
    """,
    parameters=[
        OpenApiParameter(
            name="Authorization",
            description="Authorization access token",
            required=True,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.HEADER,
        ),
    ],
)
class UserInfoAPI(generics.RetrieveAPIView):
    """
    API endpoint for retrieving user information.
    Requires a valid JWT access token.
    """

    serializer_class = UserInfoSerializer
    permission_classes = [IsAuthenticated]
    # JWTAuthentication가 요청 헤더에서 access_token을 자동으로 추출하고 유효성 검사
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        logger.info("GET /api/v1/users/info")
        user = self.request.user
        serializer = self.get_serializer(user)
        logger.info(f"User data fetched successfully for user: {user.email}")
        return Response(
            data={
                "message": "User data fetched successfully",
                "user": {
                    "username": serializer.data["username"],
                    "email": serializer.data["email"],
                    "profile_image": serializer.data["profile_image"],
                    "is_staff": serializer.data["is_staff"],
                    "oauth_platform": serializer.data.get("oauth_platform", None),
                },
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["User"],
    summary="User email activation API",
    description="""
        This API endpoint processes the user's email activation link.

        ## Key Features:
        - **Email Confirmation**: Confirms the user's email using the provided token.
        - **Account Activation**: Activates the user's account if the email is successfully confirmed.

        ## Parameters:
        - **token**: The email activation token (required).

        ## Response:
        - **200 OK**: User activated successfully and redirected to the activation page.
        - **400 Bad Request**: Invalid or expired activation code.
        - **404 Not Found**: User not found.

        ## Example:
        ### Request:
        ```
        GET /api/v1/users/activate/{token}/
        ```

        ### Response (success):
        Redirects to the activation page.

        ### Response (failure):
        ```
        {
            "message": "Invalid or Expired activation code"
        }
        ```
    """,
)
class UserEmailActivationAPI(generics.GenericAPIView):
    """
    API endpoint for processing user email activation links.
    """

    serializer_class = EmptySerializer
    permission_classes = [AllowAny]

    def get(self, request, token, *args, **kwargs) -> Union[Response, HttpResponseRedirect]:
        logger.info(f"GET /api/v1/users/activate/{token}")
        email = confirm_email_token(token)
        if email:
            try:
                user = User.objects.filter(email=email).first()
                if user is None:
                    logger.error(f"User not found for email: {email}")
                    return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
                user.is_active = True
                user.save()  # user's is_active status has changed False to True, save changes into the database
                logger.info(f"User {email} activated successfully.")
                return redirect(f"{os.getenv('MAIN_DOMAIN')}/activate/{token}")
            except User.DoesNotExist:
                logger.error(f"User does not exist for email: {email}")
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        logger.error(f"Invalid or expired activation code for token: {token}")
        return Response({"message": "Invalid or Expired activation code"}, status=status.HTTP_400_BAD_REQUEST)
