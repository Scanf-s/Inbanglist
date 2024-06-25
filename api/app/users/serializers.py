from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .utils import generate_email_token, send_activation_email


class UserRegisterSerializer(serializers.ModelSerializer):
    # 비밀번호 필드를 추가하고, 이 필드를 write_only로 설정하여 응답에 포함되지 않도록 설정
    password = serializers.CharField(write_only=True)
    password_verify = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']).exists(): # if there is a user with the same email in the database
            raise serializers.ValidationError("Email already exists")
        if attrs["password"] != attrs["password_verify"]: # if user inputs different passwords
            raise serializers.ValidationError("Password does not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_verify")  # validated_data에서 password_verify를 제거
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            is_active=False, # 이메일 인증을 하기 이전이므로 False로 설정
        )
        token = generate_email_token(user.email)
        send_activation_email(user.email, token)
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
    refresh = serializers.CharField() # if client requests logout, client must send their refresh token

    def validate(self, attrs):
        """
        In the attrs dictionary, there is all the data transferred to the serializer.
        When UserLoginAPIView's logout function passes the token to the serializer,
        the token can be retrieved from attrs['refresh']
        """
        token = attrs["refresh"]
        if not token:
            raise serializers.ValidationError("Token not found")

        try:
            # Verify that the token is not expired
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


class EmptySerializer(serializers.Serializer):
    """
    Use empty serializer to resolve errors in user email verification api
    """
    pass
