from django.urls import path
from youtube import views

urlpatterns = [
    path('', views.YoutubeList.as_view(), name='video_list'),
]