from django.contrib import admin

from accounts.models import Account, Transaction


class AccountAdmin(admin.ModelAdmin):
    pass


class TransactionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
