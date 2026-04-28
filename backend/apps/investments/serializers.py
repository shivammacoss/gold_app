from rest_framework import serializers

from .models import InvestmentPlan, UserInvestment


class InvestmentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPlan
        fields = [
            "id", "name", "description", "min_amount", "max_amount",
            "daily_roi_percent", "duration_days", "is_active",
        ]


class UserInvestmentSerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source="plan.name", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = UserInvestment
        fields = [
            "id", "user_email", "plan", "plan_name", "wallet", "amount",
            "total_earned", "daily_earning", "days_completed",
            "status", "started_at", "expires_at", "created_at",
        ]
        read_only_fields = [
            "id", "total_earned", "daily_earning", "days_completed",
            "status", "started_at", "expires_at", "created_at",
        ]


class InvestCreateSerializer(serializers.Serializer):
    plan_id = serializers.UUIDField()
    wallet_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=20, decimal_places=6)
