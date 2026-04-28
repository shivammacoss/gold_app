from decimal import Decimal

from django.conf import settings
from django.db import models

from core.models import BaseModel


class InvestmentPlan(BaseModel):
    """Admin-defined investment plans users can subscribe to."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    min_amount = models.DecimalField(max_digits=20, decimal_places=6, default=Decimal("10.000000"))
    max_amount = models.DecimalField(max_digits=20, decimal_places=6, default=Decimal("100000.000000"))
    daily_roi_percent = models.DecimalField(max_digits=6, decimal_places=3, default=Decimal("0.500"))
    duration_days = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Investment Plan"
        verbose_name_plural = "Investment Plans"
        ordering = ["min_amount"]

    def __str__(self):
        return f"{self.name} — {self.daily_roi_percent}% daily for {self.duration_days} days"


class UserInvestment(BaseModel):
    """Tracks a user's active or past investment."""

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="investments",
    )
    plan = models.ForeignKey(
        InvestmentPlan,
        on_delete=models.PROTECT,
        related_name="subscriptions",
    )
    wallet = models.ForeignKey(
        "wallets.Wallet",
        on_delete=models.CASCADE,
        related_name="investments",
    )
    amount = models.DecimalField(max_digits=20, decimal_places=6)
    total_earned = models.DecimalField(max_digits=20, decimal_places=6, default=Decimal("0.000000"))
    daily_earning = models.DecimalField(max_digits=20, decimal_places=6, default=Decimal("0.000000"))
    days_completed = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        verbose_name = "User Investment"
        verbose_name_plural = "User Investments"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} — {self.plan.name} — {self.amount} USDT — {self.status}"
