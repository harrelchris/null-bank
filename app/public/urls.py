from django.urls import path

from public import views

app_name = "public"

urlpatterns = [
    path(route="", view=views.IndexView.as_view(), name="index"),
    path(route="about/", view=views.AboutView.as_view(), name="about"),
    path(route="accessibility/", view=views.AccessibilityView.as_view(), name="accessibility"),
    path(route="careers/", view=views.CareersView.as_view(), name="careers"),
    path(route="contact/", view=views.ContactView.as_view(), name="contact"),
    path(route="cookies/", view=views.CookiesView.as_view(), name="cookies"),
    path(route="disclaimer/", view=views.DisclaimerView.as_view(), name="disclaimer"),
    path(route="knowledge/", view=views.KnowledgeView.as_view(), name="knowledge"),
    path(route="legal/", view=views.LegalView.as_view(), name="legal"),
    path(route="locations/", view=views.LocationsView.as_view(), name="locations"),
    path(route="news/", view=views.NewsView.as_view(), name="news"),
    path(route="privacy/", view=views.PrivacyView.as_view(), name="privacy"),
    path(route="questions/", view=views.QuestionsView.as_view(), name="questions"),
    path(route="security/", view=views.SecurityView.as_view(), name="security"),
    path(route="terms/", view=views.TermsView.as_view(), name="terms"),
]
