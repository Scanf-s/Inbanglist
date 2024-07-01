from django.urls import path

from s3.views import UploadProfileImageView

urlpatterns = [
    path("profile-image/upload", UploadProfileImageView.as_view(), name="profile_image_upload"),
]
