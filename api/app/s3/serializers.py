from rest_framework import serializers


class UploadProfileImageSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(write_only=True)
    class Meta:
        model = None
        fields = ["profile_image"]