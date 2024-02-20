from datetime import timedelta
from functools import cached_property

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from common.models import BaseModel


class User(AbstractUser, BaseModel):
    is_verified = models.BooleanField(default=False)
    verification_subject_template = "users/email_verification_subject.txt"
    verification_message_template = "users/email_verification_email.html"

    def get_fresh_token(self):
        VerificationToken.objects.filter(user=self).delete()
        return VerificationToken.objects.create(user=self)

    def send_verification(self, request: HttpRequest):
        if self.is_verified:
            return False
        token = self.get_fresh_token()

        scheme = "https" if settings.EMAIL_USE_TLS else "http"
        host = request.get_host()
        path = reverse("users:email_verify", kwargs={"token": token.to_string})
        verification_url = f"{ scheme }://{ host }{ path }"

        context = {
            "verification_url": verification_url,
        }
        subject = render_to_string(template_name=self.verification_subject_template)
        message = render_to_string(template_name=self.verification_message_template, context=context)
        self.email_user(subject=subject, message=message, from_email=settings.EMAIL_FROM_ADDRESS)


class VerificationToken(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="verification_token")

    def __str__(self):
        return f"Verification token - { self.user.username }"

    @cached_property
    def to_string(self):
        return str(self.uuid)

    @property
    def is_expired(self):
        return self.created_at < timezone.now() - timedelta(hours=24)

    def consume(self):
        self.user.is_verified = True
        self.user.save()
        self.delete()
