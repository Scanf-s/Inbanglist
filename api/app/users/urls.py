from django.urls import path
from users.views import UserRegisterAPI, UserLoginAPI, UserLogoutAPI, UserDeleteAPI

urlpatterns = [
    path('register/', UserRegisterAPI.as_view(), name='user_register'),
    path('login/', UserLoginAPI.as_view(), name='user_login'),
    path('logout/', UserLogoutAPI.as_view(), name='user_logout'),
    path('delete/', UserDeleteAPI.as_view(), name='user_delete'),
]