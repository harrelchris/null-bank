from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from users.models import User, VerificationToken


class UserAdmin(AuthUserAdmin):
    list_display = AuthUserAdmin.list_display + ("is_verified",)
    fieldsets = AuthUserAdmin.fieldsets + (("Verification", {"fields": ("is_verified",)}),)
    list_filter = AuthUserAdmin.list_filter + ("is_verified",)


class VerificationTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "is_expired")
    search_fields = ("user__email",)


admin.site.register(User, UserAdmin)
admin.site.register(VerificationToken, VerificationTokenAdmin)
