from rest_framework import serializers

from .models import Withdrawal


class WithdrawalSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Withdrawal
        fields = [
            "id", "user_email", "wallet", "amount", "fee", "net_amount",
            "to_address", "network", "tx_hash", "status",
            "rejection_reason", "completed_at", "created_at",
        ]
        read_only_fields = [
            "id", "fee", "net_amount", "tx_hash", "status",
            "rejection_reason", "completed_at", "created_at",
        ]


class WithdrawalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = ["wallet", "amount", "to_address", "network"]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate_to_address(self, value):
        if not value or len(value) < 20:
            raise serializers.ValidationError("Invalid withdrawal address.")
        return value
