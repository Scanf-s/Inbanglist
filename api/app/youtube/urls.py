from django.urls import path

from youtube import views

urlpatterns = [
    path("", views.YoutubeListAPI.as_view({"get": "list"}), name="youtube_list"),
    path(
        "<int:pk>",
        views.YoutubeListAPI.as_view({"get": "retrieve"}),
        name="youtube_detail",
    ),
]
