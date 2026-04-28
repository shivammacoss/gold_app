from .models import Transaction


class TransactionService:
    """Service for creating transaction ledger entries."""

    @staticmethod
    def create_transaction(user, tx_type, amount, reference_id="", description=""):
        return Transaction.objects.create(
            user=user,
            tx_type=tx_type,
            amount=amount,
            reference_id=reference_id,
            description=description,
        )

    @staticmethod
    def get_user_transactions(user, tx_type=None):
        qs = Transaction.objects.filter(user=user)
        if tx_type:
            qs = qs.filter(tx_type=tx_type)
        return qs
