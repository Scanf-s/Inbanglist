from __future__ import annotations

import logging
import os

import requests
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.utils import timezone
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from users.models import User, UserOAuth2Platform
from users.serializers import EmptySerializer, UserSocialAccountDeleteSerializer
from users.utils import get_jwt_tokens_for_user

logger = logging.getLogger(__name__)


@extend_schema(
    tags=["User/OAuth2"],
    summary="Social account user deletion API",
    description="""
        This API endpoint allows a user to delete their social account.
        ** 만약, 일반 이메일 계정에 소셜 로그인 계정으로 연동했다면,** 
        ** 해당 API는 소셜 연동만 삭제 처리되므로, **
        ** 이후 사용자 자체를 삭제하고 싶다면, Users의 delete method 사용 바랍니다. **

        ## Key Features:
        - **Authentication**: Requires a valid JWT access token.
        - **Token Blacklisting**: Adds the refresh token to the blacklist to invalidate it.
        - **Account Deletion**: Deletes the user's account from the database.

        ## Parameters:
        - **Authorization**: The access token of the user (required, in header).
        - **email**: The email address of the user (required).
        - **refresh_token**: The refresh token of the user (required).
        - **oauth_platform**: The OAuth platform used by the user (e.g., google, naver) (required).

        ## Response:
        - **200 OK**: User deleted successfully.
        - **400 Bad Request**: Invalid token or other errors.
        - **404 Not Found**: User not found.

        ## Example:
        ### Request:
        ```
        DELETE /api/v1/users/social/delete/
        Headers: {
            "Authorization": "Bearer access_token"
        }
        {
            "email": "user@example.com",
            "refresh_token": "refresh_token_string",
            "oauth_platform": "google"
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
            "message": "Invalid refresh token",
            "error": "Token is invalid or expired"
        }
        ```
    """,
    parameters=[
        OpenApiParameter(
            name="Authorization",
            description="Authorization token",
            required=True,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.HEADER,
        ),
        OpenApiParameter(name="email", description="Email of the user", required=True, type=OpenApiTypes.STR),
        OpenApiParameter(
            name="refresh_token", description="Refresh token of the user", required=True, type=OpenApiTypes.STR
        ),
        OpenApiParameter(
            name="oauth_platform",
            description="OAuth platform (e.g., google, naver) none : email signed up user",
            required=True,
            type=OpenApiTypes.STR,
        ),
    ],
)
class UserSocialDeleteAPI(generics.GenericAPIView):
    """
    API endpoint for deleting a social account user.
    Requires login and a valid JWT token in the Authorization header.
    """

    serializer_class = UserSocialAccountDeleteSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def delete(self, request, *args, **kwargs):
        logger.info("DELETE /api/v1/users/social/delete")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                email = serializer.validated_data["email"]
                refresh_token = serializer.validated_data["refresh_token"]
                oauth_platform = serializer.validated_data["oauth_platform"]
                user_oauth = UserOAuth2Platform.objects.get(user__email=email, oauth_platform=oauth_platform)
                user = user_oauth.user

                # RefreshToken을 블랙리스트에 추가
                try:
                    refresh_token_instance = RefreshToken(refresh_token)
                    refresh_token_instance.blacklist()
                except TokenError as e:
                    logger.error(f"Invalid refresh token: {str(e)}")
                    return Response(
                        {"message": "Invalid refresh token", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST
                    )

                # 사용자가 소유한 모든 OutstandingToken 삭제
                OutstandingToken.objects.filter(user=user).delete()

                # 소셜 계정 정보 삭제
                user_oauth.delete()

                # 만약 사용자가 더 이상 다른 소셜 계정이 없고, 일반 계정도 없다면 사용자 삭제
                if not UserOAuth2Platform.objects.filter(user=user).exists():
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
    tags=["User/OAuth2"],
    summary="Initiate Naver OAuth2 login process",
    description="""
        This API endpoint initiates the Naver OAuth2 login process.
        It redirects the user to the Naver login page.

        ## Key Features:
        - **Redirection**: Redirects the user to Naver's login page.
        - **OAuth2 Flow**: Starts the OAuth2 flow by requesting an authorization code from Naver.

        ## Parameters:
        - None

        ## Response:
        - **302 Found**: Redirects to Naver's login page.

        ## Example:
        ### Request:
        ```
        GET /api/v1/users/oauth2/naver/login/
        ```

        ### Response:
        Redirects to Naver login page.
    """,
)
class UserNaverLoginAPI(generics.GenericAPIView):
    """
    This API initiates the Naver OAuth2 login process.
    It redirects the user to the Naver login page.
    """

    serializer_class = EmptySerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        logger.info("GET /api/v1/users/oauth2/naver/login")
        response_type = "code"
        naver_client_id = os.getenv("NAVER_CLIENT_ID")
        if not naver_client_id:
            logger.error("NAVER_CLIENT_ID is not set")
            raise ImproperlyConfigured("NAVER_CLIENT_ID is not set")

        main_domain = os.getenv("MAIN_DOMAIN")
        if not main_domain:
            logger.error("MAIN_DOMAIN is not set")
            raise ImproperlyConfigured("MAIN_DOMAIN is not set")

        redirect_uri = main_domain + "/api/users/oauth2/naver/callback"

        state = os.getenv("NAVER_CSRF_STATE")
        if not state:
            logger.error("NAVER_CSRF_STATE is not set")
            raise ImproperlyConfigured("NAVER_STATE is not set")

        # Naver Document 에서 확인했던 요청 url
        # https://developers.naver.com/docs/login/api/api.md
        url = "https://nid.naver.com/oauth2.0/authorize"

        # 네이버 로그인 서버로 요청
        logger.info("Redirecting to Naver login page")
        return redirect(
            f"{url}?response_type={response_type}&client_id={naver_client_id}&redirect_uri={redirect_uri}&state={state}"
        )


@extend_schema(
    tags=["User/OAuth2"],
    summary="Naver OAuth2 login callback",
    description="""
        This API endpoint processes the Naver OAuth2 login callback.

        ## Key Features:
        - **Token Exchange**: Exchanges the authorization code for an access token.
        - **User Information Retrieval**: Fetches the user's profile information using the access token.
        - **User Login/Registration**: Logs in the user or creates a new user if not already registered.
        - **JWT Token Generation**: Generates JWT tokens (access and refresh) upon successful login.

        ## Parameters:
        - **code**: The authorization code provided by Naver (required, in query parameter).
        - **state**: The CSRF state value (required, in query parameter).

        ## Response:
        - **200 OK**: User logged in successfully and JWT tokens returned.
        - **400 Bad Request**: Missing or invalid parameters, or failure in token exchange.
        - **500 Internal Server Error**: Failure in user creation or login.

        ## Example:
        ### Request:
        ```
        GET /api/v1/users/oauth2/naver/callback/?code=authorization_code&state=csrf_state
        ```

        ### Response (success):
        ```
        {
            "message": "User logged in successfully",
            "access_token": "access_token_string",
            "refresh_token": "refresh_token_string"
        }
        ```

        ### Response (failure):
        ```
        {
            "message": "Authorization code is missing"
        }
        ```
    """,
)
class UserNaverLoginCallBackAPI(generics.GenericAPIView):
    """
    This API endpoint processes the Naver OAuth2 login callback.
    """

    serializer_class = EmptySerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # https://developers.naver.com/docs/login/api/api.md
        logger.info("GET /api/v1/users/oauth2/naver/callback")

        naver_client_id = os.getenv("NAVER_CLIENT_ID")
        naver_client_secret = os.getenv("NAVER_CLIENT_SECRET")
        state = os.getenv("NAVER_CSRF_STATE")

        if not naver_client_id:
            logger.error("NAVER_CLIENT_ID is not set")
            raise ImproperlyConfigured("NAVER_CLIENT_ID is not set")
        if not naver_client_secret:
            logger.error("NAVER_CLIENT_SECRET is not set")
            raise ImproperlyConfigured("NAVER_CLIENT_SECRET is not set")
        if not state:
            logger.error("NAVER_CSRF_STATE is not set")
            raise ImproperlyConfigured("NAVER_CSRF_STATE is not set")

        authorization_code = request.GET.get("code")
        received_state = request.GET.get("state")

        if not authorization_code:
            logger.error("Authorization code is missing")
            return Response({"message": "Authorization code is missing"}, status=status.HTTP_400_BAD_REQUEST)
        if received_state != state:
            logger.error("State value does not match")
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
            logger.error("Failed to get access token")
            return Response({"message": "Failed to get access token"}, status=status.HTTP_400_BAD_REQUEST)

        token_data = token_response.json()
        access_token = token_data.get("access_token")
        if not access_token:
            logger.error("Failed to get access token from token data")
            return Response({"message": "Failed to get access token"}, status=status.HTTP_400_BAD_REQUEST)

        # url, headers 설정하고, 해당 링크로 사용자 프로필 정보 요청 request
        # https://developers.naver.com/docs/login/profile/profile.md
        user_profile_request_url = "https://openapi.naver.com/v1/nid/me"
        headers = {"Authorization": f"Bearer {access_token}"}

        user_response = requests.get(user_profile_request_url, headers=headers)
        if user_response.status_code != 200:
            logger.error("Failed to get user info")
            return Response({"message": "Failed to get user info"}, status=status.HTTP_400_BAD_REQUEST)

        # 네이버 이메일을 가져와야 하는데 왜 다른 이메일이 표시되는건가요?
        # https://developers.naver.com/forum/posts/28835
        user_info = user_response.json()
        user_id = user_info.get("response", {}).get("id")
        user_email = user_info.get("response", {}).get("email")
        if not user_id or not user_email:
            logger.error("Failed to get user info from user response")
            return Response({"message": "Failed to get user info"}, status=status.HTTP_400_BAD_REQUEST)

        # 사용자 존재 여부 확인해서 새로운 사용자를 생성하거나 기존 사용자가 있다면, 로그인
        try:
            user_oauth2 = (
                UserOAuth2Platform.objects.select_related("user")
                .filter(user__email=user_email, oauth_platform="naver")
                .first()
            )

            if user_oauth2:
                # 이미 존재하는 사용자의 경우
                user = user_oauth2.user
                user.last_login = timezone.now()
                user.is_active = True
                user.save()
                logger.info(f"Existing user logged in: {user_email}")
            else:
                # 사용자가 존재하지만 소셜 계정이 연결되지 않은 경우
                user = User.objects.filter(email=user_email).first()
                if user:
                    # 기존 사용자에 소셜 계정 연결
                    UserOAuth2Platform.objects.create(user=user, oauth_platform="naver", oauth2_user_id=user_id)
                    user.last_login = timezone.now()
                    user.is_active = True
                    user.save()
                    logger.info(f"Social account linked for existing user: {user_email}")
                else:
                    # 새로운 사용자의 경우
                    user = User.objects.create_user(
                        email=user_email,
                        username=user_email.split("@")[0],
                        profile_image=os.getenv("DEFAULT_PROFILE_IMAGE_URL"),
                        last_login=timezone.now(),
                        is_active=True,
                    )
                    UserOAuth2Platform.objects.create(user=user, oauth_platform="naver", oauth2_user_id=user_id)
                    logger.info(f"New user created: {user_email}")

        except Exception as e:
            logger.error(f"Failed to get or create user: {str(e)}")
            return Response(
                {"message": "Failed to get or create user", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        tokens = get_jwt_tokens_for_user(user)

        logger.info(f"User logged in successfully: {user_email}")
        return redirect(
            f"{os.getenv('MAIN_DOMAIN')}/auth/callback?access_token={tokens['access']}&refresh_token={tokens['refresh']}"
        )


@extend_schema(
    tags=["User/OAuth2"],
    summary="Initiate Google OAuth2 login process",
    description="""
        This API endpoint initiates the Google OAuth2 login process.
        It redirects the user to the Google login page.

        ## Key Features:
        - **Redirection**: Redirects the user to Google's login page.
        - **OAuth2 Flow**: Starts the OAuth2 flow by requesting an authorization code from Google.

        ## Parameters:
        - None

        ## Response:
        - **302 Found**: Redirects to Google's login page.

        ## Example:
        ### Request:
        ```
        GET /api/v1/users/oauth2/google/login/
        ```

        ### Response:
        Redirects to Google login page.
    """,
)
class UserGoogleLoginAPI(generics.GenericAPIView):
    """
    This API initiates the Google OAuth2 login process.
    It redirects the user to the Google login page.
    """

    serializer_class = EmptySerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        logger.info("GET /api/v1/users/oauth2/google/login")
        google_client_id = os.getenv("GOOGLE_CLIENT_ID")

        if not google_client_id:
            logger.error("GOOGLE_CLIENT_ID is not set")
            raise ImproperlyConfigured("GOOGLE_CLIENT_ID is not set")

        main_domain = os.getenv("MAIN_DOMAIN")
        if not main_domain:
            logger.error("MAIN_DOMAIN is not set")
            raise ImproperlyConfigured("MAIN_DOMAIN is not set")

        state = os.getenv("GOOGLE_CSRF_STATE")
        if not state:
            logger.error("GOOGLE_CSRF_STATE is not set")
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

        logger.info("Redirecting to Google login page")
        return redirect(google_auth_url)


@extend_schema(
    tags=["User/OAuth2"],
    summary="Google OAuth2 login callback",
    description="""
        This API endpoint processes the Google OAuth2 login callback.

        ## Key Features:
        - **Token Exchange**: Exchanges the authorization code for an access token.
        - **User Information Retrieval**: Fetches the user's profile information using the access token.
        - **User Login/Registration**: Logs in the user or creates a new user if not already registered.
        - **JWT Token Generation**: Generates JWT tokens (access and refresh) upon successful login.

        ## Parameters:
        - **code**: The authorization code provided by Google (required, in query parameter).
        - **state**: The CSRF state value (required, in query parameter).

        ## Response:
        - **200 OK**: User logged in successfully and JWT tokens returned.
        - **400 Bad Request**: Missing or invalid parameters, or failure in token exchange.
        - **500 Internal Server Error**: Failure in user creation or login.

        ## Example:
        ### Request:
        ```
        GET /api/v1/users/oauth2/google/callback/?code=authorization_code&state=csrf_state
        ```

        ### Response (success):
        ```
        {
            "message": "User logged in successfully",
            "access_token": "access_token_string",
            "refresh_token": "refresh_token_string"
        }
        ```

        ### Response (failure):
        ```
        {
            "message": "Authorization code is missing"
        }
        ```
    """,
)
class UserGoogleLoginCallBackAPI(generics.GenericAPIView):
    """
    This API endpoint processes the Google OAuth2 login callback.
    """

    serializer_class = EmptySerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        logger.info("GET /api/v1/users/oauth2/google/callback")

        google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        state = os.getenv("GOOGLE_CSRF_STATE")

        if not google_client_id:
            logger.error("GOOGLE_CLIENT_ID is not set")
            raise ImproperlyConfigured("GOOGLE_CLIENT_ID is not set")
        if not google_client_secret:
            logger.error("GOOGLE_CLIENT_SECRET is not set")
            raise ImproperlyConfigured("GOOGLE_CLIENT_SECRET is not set")
        if not state:
            logger.error("GOOGLE_CSRF_STATE is not set")
            raise ImproperlyConfigured("GOOGLE_CSRF_STATE is not set")

        authorization_code = request.GET.get("code")
        received_state = request.GET.get("state")

        if not authorization_code:
            logger.error("Authorization code is missing")
            return Response({"message": "Authorization code is missing"}, status=status.HTTP_400_BAD_REQUEST)
        if received_state != state:
            logger.error("State value does not match")
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
            logger.error("Failed to get tokens")
            return Response({"message": "Failed to get access token"}, status=status.HTTP_400_BAD_REQUEST)

        token_data = token_response.json()
        access_token = token_data.get("access_token")
        id_token = token_data.get("id_token")
        if not access_token or not id_token:
            logger.error("Failed to get user info")
            return Response({"message": "Failed to get tokens"}, status=status.HTTP_400_BAD_REQUEST)

        user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}

        user_info_response = requests.get(user_info_url, headers=headers)
        if user_info_response.status_code != 200:
            logger.error("Failed to get user info")
            return Response({"message": "Failed to get user info"}, status=status.HTTP_400_BAD_REQUEST)

        user_info = user_info_response.json()
        user_id = user_info.get("sub")
        user_email = user_info.get("email")
        if not user_email or not user_id:
            logger.error("Failed to get user email and sub(id)")
            return Response({"message": "Failed to get user email and sub(id)"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_oauth2 = (
                UserOAuth2Platform.objects.select_related("user")
                .filter(user__email=user_email, oauth_platform="google")
                .first()
            )

            if user_oauth2:
                # 이미 존재하는 사용자의 경우
                user = user_oauth2.user
                user.last_login = timezone.now()
                user.is_active = True
                user.save()
                logger.info(f"Existing user logged in: {user_email}")
            else:
                # 사용자가 존재하지만 소셜 계정이 연결되지 않은 경우
                user = User.objects.filter(email=user_email).first()
                if user:
                    # 기존 사용자에 소셜 계정 연결
                    UserOAuth2Platform.objects.create(user=user, oauth_platform="google", oauth2_user_id=user_id)
                    user.last_login = timezone.now()
                    user.is_active = True
                    user.save()
                    logger.info(f"Social account linked for existing user: {user_email}")
                else:
                    # 새로운 사용자의 경우
                    user = User.objects.create_user(
                        email=user_email,
                        username=user_email.split("@")[0],
                        last_login=timezone.now(),
                        profile_image=os.getenv("DEFAULT_PROFILE_IMAGE_URL"),
                        is_active=True,
                    )
                    UserOAuth2Platform.objects.create(user=user, oauth_platform="google", oauth2_user_id=user_id)
                    logger.info(f"New user created: {user_email}")

        except Exception as e:
            logger.error(f"Failed to get or create user: {str(e)}")
            return Response(
                {"message": "Failed to get or create user", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        tokens = get_jwt_tokens_for_user(user)

        logger.info(f"User logged in successfully: {user_email}")
        return redirect(
            f"{os.getenv('MAIN_DOMAIN')}/auth/callback?access_token={tokens['access']}&refresh_token={tokens['refresh']}"
        )
