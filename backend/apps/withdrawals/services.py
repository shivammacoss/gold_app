from django.db import transaction
from django.utils import timezone

from apps.transactions.services import TransactionService
from apps.wallets.services import WalletService
from core.exceptions import InsufficientBalanceError, WithdrawalLimitExceeded

from .models import Withdrawal


class WithdrawalService:
    """Business logic for processing USDT withdrawals."""

    MINIMUM_WITHDRAWAL = 10  # USDT
    MAXIMUM_WITHDRAWAL = 50000  # USDT per transaction

    @staticmethod
    @transaction.atomic
    def create_withdrawal(user, wallet, amount, to_address, network):
        """Create a pending withdrawal request and hold funds."""
        if amount < WithdrawalService.MINIMUM_WITHDRAWAL:
            raise WithdrawalLimitExceeded(
                f"Minimum withdrawal is {WithdrawalService.MINIMUM_WITHDRAWAL} USDT."
            )
        if amount > WithdrawalService.MAXIMUM_WITHDRAWAL:
            raise WithdrawalLimitExceeded(
                f"Maximum withdrawal is {WithdrawalService.MAXIMUM_WITHDRAWAL} USDT."
            )

        # Hold funds immediately
        WalletService.debit(wallet, amount)

        withdrawal = Withdrawal.objects.create(
            user=user,
            wallet=wallet,
            amount=amount,
            to_address=to_address,
            network=network,
        )

        TransactionService.create_transaction(
            user=user,
            tx_type="WITHDRAWAL_HOLD",
            amount=amount,
            reference_id=str(withdrawal.id),
            description=f"Withdrawal hold — pending approval",
        )

        return withdrawal

    @staticmethod
    @transaction.atomic
    def approve_withdrawal(withdrawal, reviewed_by):
        """Admin approves a withdrawal for on-chain processing."""
        withdrawal.status = Withdrawal.Status.APPROVED
        withdrawal.reviewed_by = reviewed_by
        withdrawal.reviewed_at = timezone.now()
        withdrawal.save(update_fields=["status", "reviewed_by", "reviewed_at", "updated_at"])
        return withdrawal

    @staticmethod
    @transaction.atomic
    def reject_withdrawal(withdrawal, reviewed_by, reason=""):
        """Admin rejects a withdrawal — refund held funds."""
        withdrawal.status = Withdrawal.Status.REJECTED
        withdrawal.reviewed_by = reviewed_by
        withdrawal.reviewed_at = timezone.now()
        withdrawal.rejection_reason = reason
        withdrawal.save(update_fields=[
            "status", "reviewed_by", "reviewed_at", "rejection_reason", "updated_at",
        ])

        # Refund the held amount
        WalletService.credit(withdrawal.wallet, withdrawal.amount)

        TransactionService.create_transaction(
            user=withdrawal.user,
            tx_type="WITHDRAWAL_REFUND",
            amount=withdrawal.amount,
            reference_id=str(withdrawal.id),
            description=f"Withdrawal rejected — funds refunded",
        )

        return withdrawal

    @staticmethod
    @transaction.atomic
    def complete_withdrawal(withdrawal, tx_hash):
        """Mark withdrawal as completed after on-chain broadcast."""
        withdrawal.status = Withdrawal.Status.COMPLETED
        withdrawal.tx_hash = tx_hash
        withdrawal.completed_at = timezone.now()
        withdrawal.save(update_fields=["status", "tx_hash", "completed_at", "updated_at"])

        TransactionService.create_transaction(
            user=withdrawal.user,
            tx_type="WITHDRAWAL",
            amount=withdrawal.amount,
            reference_id=str(withdrawal.id),
            description=f"USDT withdrawal completed — {tx_hash}",
        )

        return withdrawal
