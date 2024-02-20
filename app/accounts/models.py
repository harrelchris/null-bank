from django.contrib.auth import get_user_model
from django.db import models

from common.models import BaseModel

User = get_user_model()

ACCOUNT_TYPES = (
    ('checking', 'Checking'),
    ('saving', 'Saving'),
    ('credit', 'Credit'),
    ('loan', 'Loan'),
)


class Account(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    available = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)


class Transaction(BaseModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    new_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    label = models.CharField(max_length=20, unique=True)
