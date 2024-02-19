from django.db import models
from django.contrib.auth import get_user_model

from common.models import BaseModel

User = get_user_model()


class Contact(BaseModel):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    message = models.TextField()
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} - {self.message[:20]}"


class Question(BaseModel):
    question = models.CharField(max_length=512)
    answer = models.TextField()

    def __str__(self):
        return self.question[:20]
