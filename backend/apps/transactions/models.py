from django.conf import settings
from django.db import models

from core.models import BaseModel


class Transaction(BaseModel):
    """Unified audit log for all financial operations."""

    class Type(models.TextChoices):
        DEPOSIT = "DEPOSIT", "Deposit"
        WITHDRAWAL = "WITHDRAWAL", "Withdrawal"
        WITHDRAWAL_HOLD = "WITHDRAWAL_HOLD", "Withdrawal Hold"
        WITHDRAWAL_REFUND = "WITHDRAWAL_REFUND", "Withdrawal Refund"
        INVESTMENT = "INVESTMENT", "Investment"
        INVESTMENT_RETURN = "INVESTMENT_RETURN", "Investment Return"
        ROI = "ROI", "Daily ROI"
        TRANSFER = "TRANSFER", "Internal Transfer"
        FEE = "FEE", "Platform Fee"
        BONUS = "BONUS", "Bonus / Referral"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    tx_type = models.CharField(max_length=30, choices=Type.choices, db_index=True)
    amount = models.DecimalField(max_digits=20, decimal_places=6)
    reference_id = models.CharField(max_length=255, blank=True, db_index=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "tx_type"]),
            models.Index(fields=["user", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.tx_type} — {self.amount} USDT — {self.user.email}"
