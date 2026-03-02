from django.db import models
from django.conf import settings


class NotificationType(models.TextChoices):
    ORDER_STATUS_CHANGED = "order_status_changed", "Order status changed"
    PRODUCT_STATUS_CHANGED = "product_status_changed", "Product status changed"


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    type = models.CharField(
        max_length=70,
        choices=NotificationType.choices
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return f"{self.user} - {self.type}"