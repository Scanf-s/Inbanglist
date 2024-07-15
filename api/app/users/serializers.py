import os

from django.db.models import Q
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, UserOAuth2Platform


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        email = attrs.get("email")

        # 사용자명 및 이메일이 이미 존재하는지 확인
        if User.objects.filter(Q(username=username) | Q(email=email)).exists():
            raise serializers.ValidationError("Username or Email already exists")

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            profile_image=os.getenv("DEFAULT_PROFILE_IMAGE"),
            is_active=False,  # 이메일 인증을 하기 이전이므로 False로 설정
        )
        # UserOAuth2Platform을 "none"으로 설정
        UserOAuth2Platform.objects.create(
            user=user,
            oauth_platform="none",
        )
        return user

    class Meta:
        model = User
        fields = ["username", "email", "password"]


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")

        return {"user": user}


class UserLogoutSerializer(serializers.Serializer):
    """
    if client requests logout, client must send their access token and refresh token
    """

    refresh_token = serializers.CharField()

    def validate(self, attrs):
        """
        In the attrs dictionary, there is all the data transferred to the serializer.
        When UserLoginAPIView's logout function passes the token to the serializer,
        the token can be retrieved from attrs['refresh']
        """
        refresh_token = attrs["refresh_token"]
        if not refresh_token:
            raise serializers.ValidationError("Refresh token are not found")

        try:
            # 토큰이 만료되지 않았는지 확인
            RefreshToken(refresh_token)
        except TokenError:
            raise serializers.ValidationError("Invalid token or Expired")
        return attrs

    class Meta:
        fields = ["refresh_token"]


class UserDeleteSerializer(serializers.Serializer):
    """
    Normal Account User Delete Serializer
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        refresh_token = attrs.get("refresh_token")

        if not email or not password or not refresh_token:
            raise serializers.ValidationError("Email, password, and refresh token are required")

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        # 사용자가 소셜 계정인지 확인
        user_oauth2 = UserOAuth2Platform.objects.filter(user=user).first()
        if user_oauth2 and user_oauth2.oauth_platform != "none":
            raise serializers.ValidationError(
                "Cannot delete social account via this endpoint. Use the User/OAuth2 API."
            )

        if not user.check_password(password):
            raise serializers.ValidationError("Password does not match")

        try:
            refresh_token_instance = RefreshToken(refresh_token)
        except TokenError:
            raise serializers.ValidationError("Invalid or expired refresh token")

        attrs["user"] = user
        attrs["refresh_token_instance"] = refresh_token_instance
        return attrs


class UserSocialAccountDeleteSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    refresh_token = serializers.CharField(required=True)
    oauth_platform = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        refresh_token = attrs.get("refresh_token")
        oauth_platform = attrs.get("oauth_platform")

        if not email or not refresh_token or not oauth_platform:
            raise serializers.ValidationError("Email, refresh token, and oauth platform are required")

        try:
            user_oauth = UserOAuth2Platform.objects.get(user__email=email, oauth_platform=oauth_platform)
            RefreshToken(refresh_token)
        except TokenError:
            raise serializers.ValidationError("Invalid or expired refresh token")
        except UserOAuth2Platform.DoesNotExist:
            raise serializers.ValidationError("User not found")

        return attrs


class UserOAuth2PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOAuth2Platform
        fields = ["oauth_platform", "oauth2_user_id"]


class UserInfoSerializer(serializers.ModelSerializer):
    oauth_platforms = UserOAuth2PlatformSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "profile_image", "oauth_platforms", "is_staff"]


class EmptySerializer(serializers.Serializer):
    """
    Use empty serializer to resolve errors in user email verification api
    """

    pass
