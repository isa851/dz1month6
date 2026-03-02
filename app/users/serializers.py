from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import serializers
from .models import PasswordResetCode
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RequestResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь не найден")
        return value

    def save(self):
        email = self.validated_data["email"]
        user = User.objects.get(email=email)

        PasswordResetCode.objects.filter(user=user).delete()

        code = PasswordResetCode.generate_code()

        PasswordResetCode.objects.create(
            user=user,
            code=code
        )

        send_mail(
            subject="Сброс пароля",
            message=f"Ваш код для сброса пароля: {code}",
            from_email=None,
            recipient_list=[email],
        )


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get("email")
        code = attrs.get("code")

        try:
            user = User.objects.get(email=email)
            reset_code = PasswordResetCode.objects.get(user=user, code=code)
        except (User.DoesNotExist, PasswordResetCode.DoesNotExist):
            raise serializers.ValidationError("Неверный код")

        if reset_code.is_expired():
            raise serializers.ValidationError("Код истёк")

        reset_code.is_verified = True
        reset_code.save(update_fields=["is_verified"])

        attrs["user"] = user
        return attrs


class SetNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")

        try:
            user = User.objects.get(email=email)
            reset_code = PasswordResetCode.objects.filter(
                user=user,
                is_verified=True
            ).latest("created_at")
        except Exception:
            raise serializers.ValidationError("Код не подтвержден")

        if reset_code.is_expired():
            raise serializers.ValidationError("Код истёк")

        attrs["user"] = user
        return attrs

    def save(self):
        user = self.validated_data["user"]
        password = self.validated_data["password"]

        user.set_password(password)
        user.save()

        PasswordResetCode.objects.filter(user=user).delete()


class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name',
            'last_name',
            'created_at', 'password'
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name',
            'last_name', 'is_active', 'is_staff', 
            'created_at'
        ]

class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod 
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        return token
        
    def validate(self, attrs):
        data = super().validate(attrs)
        data["role "] = self.user.role
        data["user_id"] = self.user.id
        data["email"] = self.user.email
        return data