from django.contrib import admin

from accounts.models import Account, Transaction


class AccountAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "name", "balance", "available")
    list_filter = ("type",)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("account", "amount", "label", "created_at")
    list_filter = ("type",)


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
