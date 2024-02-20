from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, RedirectView

from users import forms
from users.mixins import LoginProhibitedMixin
from users.models import VerificationToken


class RegisterView(LoginProhibitedMixin, FormView):
    template_name = "users/register.html"
    form_class = forms.RegisterForm
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        user = form.save()
        user.send_verification(request=self.request)
        login(self.request, user)
        messages.success(self.request, "Account created. Please check your email for a verification link.")
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = "users/profile.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        return self.request.user


class DeleteView(LoginRequiredMixin, FormView):
    template_name = "users/delete.html"
    context_object_name = "user"
    form_class = forms.DeleteForm
    success_url = reverse_lazy(settings.LOGOUT_REDIRECT_URL)

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        # TODO: prohibit user deletion if user has banking accounts
        self.request.user.delete()
        messages.success(self.request, "Your user account has been deleted.")
        return super().form_valid(form)


class LoginView(LoginProhibitedMixin, auth_views.LoginView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        if not form.cleaned_data.get("remember", False):
            self.request.session.set_expiry(0)
        return super().form_valid(form=form)


class LogoutView(auth_views.LogoutView):
    """Preserve simple ability to modify flow later if needed"""

    pass


class EmailVerifyView(RedirectView):
    url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
    http_method_names = [
        "get",
        "head",
        "options",
        "trace",
    ]

    def get(self, request, *args, **kwargs):
        token = VerificationToken.objects.get(uuid=self.kwargs.get("token"))
        if token is None:
            messages.error(request, "That link is invalid.")
        elif token.is_expired:
            token.delete()
            messages.error(request, "That link has expired. Please request a new one.")
        else:
            token.consume()
            messages.success(request, "Your email has been verified.")
        return super().get(request, *args, **kwargs)


class EmailVerifyResendView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
    http_method_names = [
        "get",
        "head",
        "options",
        "trace",
    ]

    def get(self, request, *args, **kwargs):
        request.user.send_verification(request)
        messages.success(request, "A new verification email was sent.")
        return super().get(request, *args, **kwargs)


class EmailChangeView(LoginRequiredMixin, FormView):
    form_class = forms.EmailChangeForm
    template_name = "users/email_change.html"
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    # TODO: modify flow to keep current email until new email is verified
    # verification token may hold new email until consumed
    def form_valid(self, form):
        new_email = form.cleaned_data["email"]
        if new_email == self.request.user.email:
            form.add_error("email", "This is your current email address.")
            return super().form_invalid(form)
        self.request.user.email = form.cleaned_data["email"]
        self.request.user.is_verified = False
        self.request.user.save()
        self.request.user.send_verification(request=self.request)  # noqa
        messages.success(self.request, "Email address changed. Please check your email for a verification link.")
        return super().form_valid(form)


class PasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = "users/password_change.html"
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
    form_class = forms.PasswordChangeForm

    def form_valid(self, form):
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, "Password changed.")
        return super().form_valid(form)


class PasswordResetView(LoginProhibitedMixin, auth_views.PasswordResetView):
    template_name = "users/password_reset.html"
    form_class = forms.PasswordResetForm
    email_template_name = "users/password_reset_email.html"
    subject_template_name = "users/password_reset_subject.txt"
    success_url = reverse_lazy("users:password_reset")

    def form_valid(self, form):
        messages.success(self.request, "Password reset request received.")
        return super().form_valid(form)


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = forms.PasswordResetConfirmForm
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
    template_name = "users/password_reset_confirm.html"

    def dispatch(self, *args, **kwargs):
        """The default flow is poorly engineered.
        Redesigned to allow redirect on invalid link,
        rather than requiring a single template with
        two possible displays.
        """

        response = super().dispatch(*args, **kwargs)
        token = kwargs["token"]
        session_token = self.request.session.get(auth_views.INTERNAL_RESET_SESSION_TOKEN)
        if token != "set-password" and not self.token_generator.check_token(self.user, session_token):
            messages.error(self.request, message="Invalid Link")
            return redirect("users:password_reset")
        return response

    def form_valid(self, form):
        messages.success(self.request, "Password reset. Please log in")
        return super().form_valid(form)
