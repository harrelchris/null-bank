from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.safestring import mark_safe

from public.models import Contact


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "autocomplete": "username",
                "autofocus": True,
                "class": "form-control",
                "placeholder": "Username",
            },
        ),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "password",
                "class": "form-control",
                "placeholder": "Password",
            },
        ),
    )
    remember = forms.BooleanField(
        label="Remember Me",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "checked": True,
                "class": "form-check-input",
            },
        ),
    )


class ContactForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "autofocus": True,
                "class": "form-control",
                "placeholder": "Email",
            },
        ),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "placeholder": "Message",
                "rows": 10,
            },
        ),
    )
    questions = forms.BooleanField(
        required=True,
        label=mark_safe("I have read the <a href='/faq/'>FAQ</a>"),
        widget=forms.CheckboxInput(
            attrs={
                "checked": False,
                "class": "form-check-input",
            },
        ),
    )

    class Meta:
        model = Contact
        fields = [
            "email",
            "message",
            "questions",
        ]
