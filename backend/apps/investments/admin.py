from django.contrib import admin

from .models import InvestmentPlan, UserInvestment


@admin.register(InvestmentPlan)
class InvestmentPlanAdmin(admin.ModelAdmin):
    list_display = ["name", "daily_roi_percent", "duration_days", "min_amount", "max_amount", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]


@admin.register(UserInvestment)
class UserInvestmentAdmin(admin.ModelAdmin):
    list_display = ["user", "plan", "amount", "total_earned", "days_completed", "status", "expires_at"]
    list_filter = ["status", "plan"]
    search_fields = ["user__email"]
    readonly_fields = ["id", "created_at", "updated_at"]
