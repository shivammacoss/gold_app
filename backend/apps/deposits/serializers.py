from rest_framework import serializers

from .models import Deposit


class DepositSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Deposit
        fields = [
            "id", "user_email", "wallet", "amount", "tx_hash",
            "from_address", "network", "confirmations",
            "required_confirmations", "status", "confirmed_at", "created_at",
        ]
        read_only_fields = [
            "id", "amount", "tx_hash", "from_address", "confirmations",
            "status", "confirmed_at", "created_at",
        ]
