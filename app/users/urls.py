from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView,
)

from app.users.views import (
    RegisterAPI,
    ProfileAPI,
    TelegramLinkCodeView,
    CustomToken,
    RequestPasswordResetView,
    VerifyCodeView,
    SetNewPasswordView
)

router = DefaultRouter()
router.register(r"register", RegisterAPI, basename="register")
router.register(r"profile", ProfileAPI, basename="profile")

router.register(r"password-reset", RequestPasswordResetView, basename="password-reset")
router.register(r"password-verify", VerifyCodeView, basename="password-verify")
router.register(r"set-new-password", SetNewPasswordView, basename="set-new-password")

urlpatterns = [
    path("token/", CustomToken.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("logout/", TokenBlacklistView.as_view()),
    # path("telegram/", TelegramLinkCodeView.as_view()),
    path("", include(router.urls)),
]