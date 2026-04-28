from django.contrib import admin

from .models import Withdrawal


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ["user", "amount", "fee", "net_amount", "network", "status", "created_at"]
    list_filter = ["status", "network"]
    search_fields = ["user__email", "to_address", "tx_hash"]
    readonly_fields = ["id", "created_at", "updated_at", "completed_at", "reviewed_at"]
    actions = ["approve_selected", "reject_selected"]

    @admin.action(description="Approve selected withdrawals")
    def approve_selected(self, request, queryset):
        from .services import WithdrawalService
        for withdrawal in queryset.filter(status=Withdrawal.Status.PENDING):
            WithdrawalService.approve_withdrawal(withdrawal, reviewed_by=request.user)

    @admin.action(description="Reject selected withdrawals")
    def reject_selected(self, request, queryset):
        from .services import WithdrawalService
        for withdrawal in queryset.filter(status=Withdrawal.Status.PENDING):
            WithdrawalService.reject_withdrawal(
                withdrawal, reviewed_by=request.user, reason="Rejected via admin"
            )
