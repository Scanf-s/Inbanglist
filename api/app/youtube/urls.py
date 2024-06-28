from django.urls import path

from youtube.views import YoutubeListAPI, YoutubeRetrieveUpdateDestroyAPI

urlpatterns = [
    path("", YoutubeListAPI.as_view(), name="youtube_list_create"),
    path("<int:pk>/", YoutubeRetrieveUpdateDestroyAPI.as_view(), name="youtube_retrieve_update_destroy"),
]
