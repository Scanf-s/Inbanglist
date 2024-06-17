from django.urls import path
from youtube import views

urlpatterns = [
    path('', views.YoutubeList.as_view(), name='youtube_list'),
    path('<int:pk>', views.YoutubeDetail.as_view(), name='youtube_detail'),
]