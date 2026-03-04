from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, PasswordResetCode, TelegramLinkCode


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "role", "is_staff", "is_active", "created_at")
    search_fields = ("email",)
    list_filter = ("role", "is_staff", "is_active")
    ordering = ("-created_at",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "role")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Dates", {"fields": ("created_at",)}),
    )

    readonly_fields = ("created_at",)


@admin.register(PasswordResetCode)
class PasswordResetCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "is_verified", "created_at")
    list_filter = ("is_verified", "created_at")


@admin.register(TelegramLinkCode)
class TelegramLinkCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "is_user", "created_at")