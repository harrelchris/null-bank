from django.contrib.auth import get_user_model
from django.db import models

from common.models import BaseModel

User = get_user_model()

ACCOUNT_TYPES = {
    "ch": "Checking",
    "sa": "Savings",
    "cr": "Credit",
    "ln": "Loan",
}

TRANSACTION_STATUSES = {
    "pg": "Pending",
    "cp": "Completed",
    "fl": "Failed",
}

TRANSACTION_TYPES = {
    "dp": "Deposit",
    "tr": "Transfer",
    "wd": "Withdrawal",
    "pt": "Payment",
}

out_going = [
    "wd",
    "pt",
]
in_coming = [
    "dp",
    "tr",
]


def generate_account_number(min_num: int = "62520120") -> int:
    last_record = Account.objects.order_by("number").last()
    if last_record:
        return last_record.number + 1
    else:
        return min_num


class Account(BaseModel):
    # TODO: add credit and lending account fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.IntegerField(default=generate_account_number, unique=True, editable=False, blank=True, null=False)
    name = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    available = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)

    def __str__(self):
        return f"{self.user} {self.get_type_display()}: {self.number} - {self.name}"


class Transaction(BaseModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, blank=False, null=False)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, blank=False, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    balance_before = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    label = models.CharField(max_length=50, blank=False, null=False)
    status = models.CharField(max_length=20, default="pending", choices=TRANSACTION_STATUSES, blank=False, null=False)

    def __str__(self):
        return f"{self.account.user} - {self.get_type_display()} - {self.amount}"

    def complete(self):
        self.status = "cp"
        super().save()
        if self.type in in_coming:
            self.account.available = self.account.available + self.amount
        elif self.type in out_going:
            self.account.available = self.account.available - self.amount
        self.account.save()
        return self

    def save(self, *args, **kwargs):
        self.balance_before = self.account.balance

        if self.type in in_coming:
            self.balance_after = self.account.balance + self.amount
        elif self.type in out_going:
            self.balance_after = self.account.balance - self.amount

        super().save(*args, **kwargs)
        self.account.balance = self.balance_after
        self.account.save()
        return self
