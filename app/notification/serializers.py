from rest_framework import serializers
from app.notification.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "type",
            "title",
            "message",
            "is_read",
            "delivered_at",
            "created_at"
        ]
        read_only_fields = ("id", "created_at", "delivered_at")