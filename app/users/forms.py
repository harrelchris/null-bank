from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model, password_validation

User = get_user_model()


class RegisterForm(auth_forms.UserCreationForm):
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
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "class": "form-control",
                "placeholder": "Email",
            }
        ),
    )
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
                "placeholder": "Password",
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
                "placeholder": "Confirm Password",
            }
        ),
        strip=False,
    )
    understand = forms.BooleanField(
        label="I agree to the Terms of Service and Privacy Policy.",
        required=True,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            },
        ),
    )
    field_order = [
        "username",
        "email",
        "password1",
        "password2",
        "understand",
    ]

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]


class DeleteForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "autofocus": True,
                "class": "form-control",
                "placeholder": "Password",
            },
        ),
    )
    understand = forms.BooleanField(
        label="I understand that this action is permanent and irreversible",
        required=True,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            },
        ),
    )

    class Meta:
        model = User
        fields = [
            "password",
            "understand",
        ]


class LoginForm(auth_forms.AuthenticationForm):
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


class EmailChangeForm(forms.ModelForm):
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
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "autofocus": True,
                "class": "form-control",
                "placeholder": "Password",
            },
        ),
    )
    understand = forms.BooleanField(
        label="I understand I will need to verify my new email address",
        required=True,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            },
        ),
    )

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "understand",
        ]


class PasswordChangeForm(auth_forms.PasswordChangeForm):
    old_password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "autofocus": True,
                "class": "form-control",
                "placeholder": "Old Password",
            },
        ),
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
                "placeholder": "New Password",
            },
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
                "placeholder": "Confirm New Password",
            },
        ),
    )
    understand = forms.BooleanField(
        label="I understand this log me out on all other devices.",
        required=True,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            },
        ),
    )
    field_order = [
        "old_password",
        "new_password1",
        "new_password2",
        "understand",
    ]


class PasswordResetForm(auth_forms.PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "autofocus": True,
                "class": "form-control",
                "placeholder": "Email",
            },
        ),
    )


class PasswordResetConfirmForm(auth_forms.SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "autofocus": True,
                "class": "form-control",
                "placeholder": "New Password",
            },
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
                "placeholder": "Confirm New Password",
            },
        ),
    )
    field_order = [
        "new_password1",
        "new_password2",
    ]
