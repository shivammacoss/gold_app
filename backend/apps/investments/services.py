from decimal import Decimal

from django.db import transaction
from django.utils import timezone
from datetime import timedelta

from apps.transactions.services import TransactionService
from apps.wallets.models import Wallet
from apps.wallets.services import WalletService
from core.exceptions import InsufficientBalanceError, InvestmentNotFoundError

from .models import InvestmentPlan, UserInvestment


class InvestmentService:
    """Business logic for investment operations."""

    @staticmethod
    @transaction.atomic
    def create_investment(user, plan_id, wallet_id, amount):
        """User subscribes to an investment plan."""
        try:
            plan = InvestmentPlan.objects.get(id=plan_id, is_active=True)
        except InvestmentPlan.DoesNotExist:
            raise InvestmentNotFoundError()

        if amount < plan.min_amount or amount > plan.max_amount:
            raise ValueError(
                f"Amount must be between {plan.min_amount} and {plan.max_amount} USDT."
            )

        wallet = Wallet.objects.get(id=wallet_id, user=user)

        # Debit investment amount from wallet
        WalletService.debit(wallet, amount)

        daily_earning = (amount * plan.daily_roi_percent) / Decimal("100")

        investment = UserInvestment.objects.create(
            user=user,
            plan=plan,
            wallet=wallet,
            amount=amount,
            daily_earning=daily_earning,
            expires_at=timezone.now() + timedelta(days=plan.duration_days),
        )

        TransactionService.create_transaction(
            user=user,
            tx_type="INVESTMENT",
            amount=amount,
            reference_id=str(investment.id),
            description=f"Invested in {plan.name}",
        )

        return investment

    @staticmethod
    @transaction.atomic
    def process_daily_returns():
        """Celery task: Credit daily ROI to all active investments."""
        active_investments = UserInvestment.objects.filter(
            status=UserInvestment.Status.ACTIVE,
            expires_at__gt=timezone.now(),
        ).select_related("wallet", "user", "plan")

        for inv in active_investments:
            WalletService.credit(inv.wallet, inv.daily_earning)
            inv.total_earned += inv.daily_earning
            inv.days_completed += 1
            inv.save(update_fields=["total_earned", "days_completed", "updated_at"])

            TransactionService.create_transaction(
                user=inv.user,
                tx_type="ROI",
                amount=inv.daily_earning,
                reference_id=str(inv.id),
                description=f"Daily ROI — {inv.plan.name}",
            )

    @staticmethod
    @transaction.atomic
    def complete_expired_investments():
        """Celery task: Mark expired investments as completed and return principal."""
        expired = UserInvestment.objects.filter(
            status=UserInvestment.Status.ACTIVE,
            expires_at__lte=timezone.now(),
        ).select_related("wallet", "user", "plan")

        for inv in expired:
            # Return principal
            WalletService.credit(inv.wallet, inv.amount)
            inv.status = UserInvestment.Status.COMPLETED
            inv.save(update_fields=["status", "updated_at"])

            TransactionService.create_transaction(
                user=inv.user,
                tx_type="INVESTMENT_RETURN",
                amount=inv.amount,
                reference_id=str(inv.id),
                description=f"Principal returned — {inv.plan.name}",
            )
