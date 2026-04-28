from django.contrib import admin

from .models import Deposit


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ["user", "amount", "network", "status", "confirmations", "created_at"]
    list_filter = ["status", "network"]
    search_fields = ["user__email", "tx_hash", "from_address"]
    readonly_fields = ["id", "created_at", "updated_at", "confirmed_at"]
