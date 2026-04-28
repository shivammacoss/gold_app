from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["user", "tx_type", "amount", "reference_id", "created_at"]
    list_filter = ["tx_type"]
    search_fields = ["user__email", "reference_id", "description"]
    readonly_fields = ["id", "created_at", "updated_at"]
    date_hierarchy = "created_at"
