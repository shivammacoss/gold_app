from rest_framework import serializers

from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Wallet
        fields = ["id", "user_email", "network", "address", "balance", "is_active", "created_at"]
        read_only_fields = ["id", "address", "balance", "created_at"]
