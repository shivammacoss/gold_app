from decimal import Decimal

from django.conf import settings
from django.db import models

from core.models import BaseModel


class Deposit(BaseModel):
    """Tracks incoming USDT deposits from blockchain."""

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending Confirmation"
        CONFIRMING = "CONFIRMING", "Confirming on Chain"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="deposits",
    )
    wallet = models.ForeignKey(
        "wallets.Wallet",
        on_delete=models.CASCADE,
        related_name="deposits",
    )
    amount = models.DecimalField(max_digits=20, decimal_places=6, default=Decimal("0.000000"))
    tx_hash = models.CharField(max_length=255, unique=True, db_index=True)
    from_address = models.CharField(max_length=255)
    network = models.CharField(max_length=10)
    confirmations = models.PositiveIntegerField(default=0)
    required_confirmations = models.PositiveIntegerField(default=20)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Deposit"
        verbose_name_plural = "Deposits"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Deposit {self.amount} USDT — {self.status} — {self.user.email}"
