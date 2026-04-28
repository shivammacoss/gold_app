from decimal import Decimal

from django.conf import settings
from django.db import models

from core.models import BaseModel


class Withdrawal(BaseModel):
    """Tracks outgoing USDT withdrawal requests."""

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending Approval"
        APPROVED = "APPROVED", "Approved"
        PROCESSING = "PROCESSING", "Processing on Chain"
        COMPLETED = "COMPLETED", "Completed"
        REJECTED = "REJECTED", "Rejected"
        FAILED = "FAILED", "Failed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="withdrawals",
    )
    wallet = models.ForeignKey(
        "wallets.Wallet",
        on_delete=models.CASCADE,
        related_name="withdrawals",
    )
    amount = models.DecimalField(max_digits=20, decimal_places=6)
    fee = models.DecimalField(max_digits=20, decimal_places=6, default=Decimal("1.000000"))
    net_amount = models.DecimalField(max_digits=20, decimal_places=6, default=Decimal("0.000000"))
    to_address = models.CharField(max_length=255)
    network = models.CharField(max_length=10)
    tx_hash = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_withdrawals",
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Withdrawal"
        verbose_name_plural = "Withdrawals"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Withdrawal {self.amount} USDT — {self.status} — {self.user.email}"

    def save(self, *args, **kwargs):
        self.net_amount = self.amount - self.fee
        super().save(*args, **kwargs)
