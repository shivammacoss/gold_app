from decimal import Decimal

from django.db import transaction

from core.exceptions import InsufficientBalanceError

from .models import Wallet


class WalletService:
    """Business logic for wallet operations."""

    @staticmethod
    def get_user_wallets(user):
        return Wallet.objects.filter(user=user, is_active=True)

    @staticmethod
    def get_or_create_wallet(user, network=Wallet.Network.TRC20):
        wallet, created = Wallet.objects.get_or_create(
            user=user,
            network=network,
            defaults={"address": ""},  # Address will be set by blockchain service
        )
        return wallet, created

    @staticmethod
    @transaction.atomic
    def credit(wallet, amount, lock=True):
        """Credit USDT to a wallet (deposit, investment return, etc.)."""
        if lock:
            wallet = Wallet.objects.select_for_update().get(pk=wallet.pk)
        wallet.balance += Decimal(str(amount))
        wallet.save(update_fields=["balance", "updated_at"])
        return wallet

    @staticmethod
    @transaction.atomic
    def debit(wallet, amount, lock=True):
        """Debit USDT from a wallet (withdrawal, investment, etc.)."""
        if lock:
            wallet = Wallet.objects.select_for_update().get(pk=wallet.pk)
        amount = Decimal(str(amount))
        if wallet.balance < amount:
            raise InsufficientBalanceError()
        wallet.balance -= amount
        wallet.save(update_fields=["balance", "updated_at"])
        return wallet

    @staticmethod
    @transaction.atomic
    def transfer(from_wallet, to_wallet, amount):
        """Internal transfer between two wallets."""
        WalletService.debit(from_wallet, amount)
        WalletService.credit(to_wallet, amount)
