from rest_framework import serializers

from users.models import User


class UploadProfileImageSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(write_only=True)

    class Meta:
        model = User
        fields = ["profile_image"]
