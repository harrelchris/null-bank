from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, TemplateView

from public.forms import ContactForm, LoginForm
from public.models import Question


class AboutView(TemplateView):
    template_name = "public/about.html"


class AccessibilityView(TemplateView):
    template_name = "public/accessibility.html"


class CareersView(TemplateView):
    template_name = "public/careers.html"


class ContactView(FormView):
    form_class = ContactForm
    template_name = "public/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["form"].fields["email"].initial = self.request.user.email
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        messages.success(self.request, "Your message has been sent.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("public:contact")


class CookiesView(TemplateView):
    template_name = "public/cookies.html"


class DisclaimerView(TemplateView):
    template_name = "public/disclaimer.html"


class IndexView(LoginView):
    template_name = "public/index.html"
    form_class = LoginForm
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        if not form.cleaned_data.get("remember", False):
            self.request.session.set_expiry(0)
        return super().form_valid(form=form)


class KnowledgeView(TemplateView):
    template_name = "public/knowledge.html"


class LegalView(TemplateView):
    template_name = "public/legal.html"


class LocationsView(TemplateView):
    template_name = "public/locations.html"


class NewsView(TemplateView):
    template_name = "public/news.html"


class PrivacyView(TemplateView):
    template_name = "public/privacy.html"


class QuestionsView(ListView):
    template_name = "public/questions.html"
    model = Question
    context_object_name = "questions"


class SecurityView(TemplateView):
    template_name = "public/security.html"


class TermsView(TemplateView):
    template_name = "public/terms.html"
