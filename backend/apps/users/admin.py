from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["email", "username", "is_kyc_verified", "is_active", "date_joined"]
    list_filter = ["is_kyc_verified", "is_active", "is_staff"]
    search_fields = ["email", "username", "phone_number"]
    ordering = ["-date_joined"]
    fieldsets = BaseUserAdmin.fieldsets + (
        ("App Fields", {"fields": ("phone_number", "is_kyc_verified", "referral_code", "referred_by")}),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "full_name", "country"]
    search_fields = ["user__email", "full_name"]
