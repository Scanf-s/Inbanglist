from django.urls import path

from users.views import UserDeleteAPI, UserLoginAPI, UserLogoutAPI, UserRegisterAPI, UserEmailActivationAPI

urlpatterns = [
    path("register/", UserRegisterAPI.as_view(), name="user_register"),
    path("login/", UserLoginAPI.as_view(), name="user_login"),
    path("logout/", UserLogoutAPI.as_view(), name="user_logout"),
    path("delete/", UserDeleteAPI.as_view(), name="user_delete"),
    path("activate/<str:token>/", UserEmailActivationAPI.as_view(), name="user_email_activate")
]
