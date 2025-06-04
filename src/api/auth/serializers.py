from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "username"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class RefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        try:
            # Стандартная валидация refresh-токена
            data = super().validate(attrs)
            
            # Получаем пользователя из refresh-токена
            refresh = RefreshToken(attrs['refresh'])
            user_id = refresh.payload.get('user_id')
            user = User.objects.get(id=user_id)

            # Дополнительная проверка: активен ли пользователь
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
            
            return data

        except InvalidToken as e:
            raise InvalidToken("Invalid or expired refresh token.")

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True, write_only=True)
    
    def validate_refresh(self, value):
        try:
            RefreshToken(value)
            return value
        except TokenError as e:
            raise serializers.ValidationError(str(e))