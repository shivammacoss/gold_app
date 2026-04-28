from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id", "user_email", "tx_type", "amount",
            "reference_id", "description", "created_at",
        ]
        read_only_fields = fields
