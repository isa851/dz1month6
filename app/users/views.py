from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from app.users.models import User, TelegramLinkCode
from app.users.serializers import (
    RegisterSerializers,
    UserProfileSerializers,
    TokenObtainPairSerializer,
    RequestResetSerializer,
    VerifyCodeSerializer,
    SetNewPasswordSerializer
)


class RequestPasswordResetView(mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RequestResetSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Код отправлен на почту"},
            status=status.HTTP_200_OK
        )


class VerifyCodeView(mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = VerifyCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"message": "Код подтвержден"},
            status=status.HTTP_200_OK
        )


class SetNewPasswordView(mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SetNewPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Пароль успешно изменён"},
            status=status.HTTP_200_OK
        )


class RegisterAPI(mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializers


class ProfileAPI(mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = UserProfileSerializers
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class TelegramLinkCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        obj, _ = TelegramLinkCode.objects.get_or_create(user=request.user)

        obj.code = TelegramLinkCode.generate_code()
        obj.is_user = False
        obj.save(update_fields=["code", "is_user"])

        return Response({"code": obj.code}, status=status.HTTP_200_OK)


class CustomToken(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
