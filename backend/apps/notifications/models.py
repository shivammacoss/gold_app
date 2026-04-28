from django.conf import settings
from django.db import models

from core.models import BaseModel


class Notification(BaseModel):
    """In-app notifications for users."""

    class Type(models.TextChoices):
        DEPOSIT_CONFIRMED = "DEPOSIT_CONFIRMED", "Deposit Confirmed"
        WITHDRAWAL_APPROVED = "WITHDRAWAL_APPROVED", "Withdrawal Approved"
        WITHDRAWAL_COMPLETED = "WITHDRAWAL_COMPLETED", "Withdrawal Completed"
        WITHDRAWAL_REJECTED = "WITHDRAWAL_REJECTED", "Withdrawal Rejected"
        INVESTMENT_CREATED = "INVESTMENT_CREATED", "Investment Created"
        INVESTMENT_COMPLETED = "INVESTMENT_COMPLETED", "Investment Completed"
        ROI_CREDITED = "ROI_CREDITED", "ROI Credited"
        SYSTEM = "SYSTEM", "System Notification"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    notification_type = models.CharField(max_length=30, choices=Type.choices)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.notification_type} — {self.user.email}"
