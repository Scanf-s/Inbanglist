from django.urls import path

from users.views.auth_views import (
    UserDeleteAPI,
    UserEmailActivationAPI,
    UserInfoAPI,
    UserLoginAPI,
    UserLogoutAPI,
    UserRegisterAPI,
)
from users.views.social_auth_views import (
    UserGoogleLoginAPI,
    UserGoogleLoginCallBackAPI,
    UserNaverLoginAPI,
    UserNaverLoginCallBackAPI,
    UserSocialDeleteAPI,
)

urlpatterns = [
    path("register", UserRegisterAPI.as_view(), name="user_register"),
    path("login", UserLoginAPI.as_view(), name="user_login"),
    path("logout", UserLogoutAPI.as_view(), name="user_logout"),
    path("delete", UserDeleteAPI.as_view(), name="user_delete"),
    path("info", UserInfoAPI.as_view(), name="user_info"),
    path("activate/<str:token>", UserEmailActivationAPI.as_view(), name="user_email_activate"),
    path("oauth2/delete", UserSocialDeleteAPI.as_view(), name="user_social_delete"),
    path("oauth2/naver/login", UserNaverLoginAPI.as_view(), name="user_oauth2_naver_login"),
    path("oauth2/naver/callback", UserNaverLoginCallBackAPI.as_view(), name="user_oauth2_naver_callback"),
    path("oauth2/google/login", UserGoogleLoginAPI.as_view(), name="user_oauth2_google_login"),
    path("oauth2/google/callback", UserGoogleLoginCallBackAPI.as_view(), name="user_oauth2_google_callback"),
]
