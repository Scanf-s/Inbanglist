from typing import Dict

from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    # 비밀번호 필드를 추가하고, 이 필드를 write_only로 설정하여 응답에 포함되지 않도록 설정
    password = serializers.CharField(write_only=True)
    password_verify = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["password"] != attrs["password_verify"]:
            raise serializers.ValidationError("Password does not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_verify")  # validated_data에서 password_verify를 제거
        user = User.objects.create_user(email=validated_data["email"], password=validated_data["password"])
        return user

    class Meta:
        model = User
        fields = ["email", "password", "password_verify"]


class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]


class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()  # 클라이언트가 로그아웃 요청 시 제공하는 Refresh Token (CharField로 받는다)

    def validate(self, attrs):
        """
        attr dictionary에는 serializer로 전달된 모든 데이터가 존재하는데,
        UserLoginAPIView의 logout 함수에서 token을 serializer로 넘겼으니까
        attrs['refresh']로 해당 값을 가져올 수 있음
        """
        token = attrs["refresh"]
        if not token:
            raise serializers.ValidationError("Token not found")

        try:
            # 유효한 토큰인지 검증
            RefreshToken(token)
        except TokenError:
            raise serializers.ValidationError("Invalid token or Expired")
        return attrs

    class Meta:
        fields = ["refresh"]


class UserDeleteSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    refresh = serializers.CharField()

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]
        token = attrs["refresh"]

        if not token or not email or not password:
            raise serializers.ValidationError("All fields are required")
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise serializers.ValidationError("Password does not match")
            RefreshToken(token)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        except TokenError:
            raise serializers.ValidationError("Invalid token or expired")
        return attrs

    class Meta:
        model = User
        fields = ["email", "password", "refresh"]
