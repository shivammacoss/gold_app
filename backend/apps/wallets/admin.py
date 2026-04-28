from django.contrib import admin

from .models import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ["user", "network", "address", "balance", "is_active", "created_at"]
    list_filter = ["network", "is_active"]
    search_fields = ["user__email", "address"]
    readonly_fields = ["id", "created_at", "updated_at"]
