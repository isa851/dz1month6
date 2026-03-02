from django.urls import path
from rest_framework.routers import DefaultRouter
from app.notification.views import NotificationReadAPI, NotificationViewSet

router = DefaultRouter()
router.register("", NotificationViewSet, basename="notifications")

read_view = NotificationReadAPI.as_view({
    "patch": "partial_update"
})

urlpatterns = [
    path("<int:pk>/read/", read_view, name="notification-read"),
]

urlpatterns += router.urls