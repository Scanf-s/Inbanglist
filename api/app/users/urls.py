from django.urls import path

from users.views import (
    UserDeleteAPI,
    UserEmailActivationAPI,
    UserGoogleLoginAPI,
    UserGoogleLoginCallBackAPI,
    UserLoginAPI,
    UserLogoutAPI,
    UserNaverLoginAPI,
    UserNaverLoginCallBackAPI,
    UserRegisterAPI,
    UserSocialDeleteAPI,
)

urlpatterns = [
    path("register/", UserRegisterAPI.as_view(), name="user_register"),
    path("login/", UserLoginAPI.as_view(), name="user_login"),
    path("logout/", UserLogoutAPI.as_view(), name="user_logout"),
    path("delete/", UserDeleteAPI.as_view(), name="user_delete"),
    path("activate/<str:token>/", UserEmailActivationAPI.as_view(), name="user_email_activate"),
    path("oauth2/delete/", UserSocialDeleteAPI.as_view(), name="user_social_delete"),
    path("oauth2/naver/login", UserNaverLoginAPI.as_view(), name="user_oauth2_naver_login"),
    path("oauth2/naver/callback", UserNaverLoginCallBackAPI.as_view(), name="user_oauth2_naver_callback"),
    path("oauth2/google/login", UserGoogleLoginAPI.as_view(), name="user_oauth2_google_login"),
    path("oauth2/google/callback", UserGoogleLoginCallBackAPI.as_view(), name="user_oauth2_google_callback"),
]
