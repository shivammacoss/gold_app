from django.db import transaction
from django.utils import timezone

from apps.transactions.services import TransactionService
from apps.wallets.services import WalletService

from .models import Deposit


class DepositService:
    """Business logic for processing USDT deposits."""

    @staticmethod
    @transaction.atomic
    def confirm_deposit(deposit: Deposit):
        """Mark deposit as completed and credit user's wallet."""
        if deposit.status == Deposit.Status.COMPLETED:
            return deposit

        deposit.status = Deposit.Status.COMPLETED
        deposit.confirmed_at = timezone.now()
        deposit.save(update_fields=["status", "confirmed_at", "updated_at"])

        WalletService.credit(deposit.wallet, deposit.amount)

        TransactionService.create_transaction(
            user=deposit.user,
            tx_type="DEPOSIT",
            amount=deposit.amount,
            reference_id=str(deposit.id),
            description=f"USDT deposit via {deposit.network}",
        )

        return deposit

    @staticmethod
    def update_confirmations(deposit: Deposit, confirmations: int):
        """Update confirmation count; auto-confirm if threshold met."""
        deposit.confirmations = confirmations
        deposit.save(update_fields=["confirmations", "updated_at"])

        if confirmations >= deposit.required_confirmations:
            DepositService.confirm_deposit(deposit)

        return deposit
