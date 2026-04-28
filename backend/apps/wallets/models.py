from decimal import Decimal

from django.conf import settings
from django.db import models

from core.models import BaseModel


class Wallet(BaseModel):
    """User's USDT wallet — internal ledger balance."""

    class Network(models.TextChoices):
        TRC20 = "TRC20", "TRON (TRC-20)"
        ERC20 = "ERC20", "Ethereum (ERC-20)"
        BEP20 = "BEP20", "BSC (BEP-20)"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wallets",
    )
    network = models.CharField(max_length=10, choices=Network.choices, default=Network.TRC20)
    address = models.CharField(max_length=255, unique=True)
    balance = models.DecimalField(max_digits=20, decimal_places=6, default=Decimal("0.000000"))
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"
        unique_together = ["user", "network"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} — {self.network} ({self.balance} USDT)"
