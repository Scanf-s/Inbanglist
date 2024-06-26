from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    # 비밀번호 필드를 추가하고, 이 필드를 write_only로 설정하여 응답에 포함되지 않도록 설정
    password = serializers.CharField(write_only=True)
    password_verify = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():  # if there is a user with the same email in the database
            raise serializers.ValidationError("Email already exists")
        if attrs["password"] != attrs["password_verify"]:  # if user inputs different passwords
            raise serializers.ValidationError("Password does not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_verify")  # validated_data에서 password_verify를 제거
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            is_active=False,  # 이메일 인증을 하기 이전이므로 False로 설정
        )
        return user

    class Meta:
        model = User
        fields = ["email", "password", "password_verify"]


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # 이메일 조회
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Email not found")

        # 비밀번호 검사
        if not user.check_password(password):
            raise serializers.ValidationError("Password does not match")

        # 사용자 활성 상태 확인
        if not user.is_active:
            raise serializers.ValidationError("User is not active. Please check your email")

        return {"user": user}

    class Meta:
        model = User
        fields = ["email", "password"]


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
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]
        refresh_token = attrs["refresh_token"]

        if not refresh_token or not email or not password:
            raise serializers.ValidationError("All fields are required")
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise serializers.ValidationError("Password does not match")
            RefreshToken(refresh_token)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        except TokenError:
            raise serializers.ValidationError("Invalid token or expired")

        return attrs

    class Meta:
        model = User
        fields = ["email", "password", "access_token", "refresh_token"]


class EmptySerializer(serializers.Serializer):
    """
    Use empty serializer to resolve errors in user email verification api
    """

    pass
