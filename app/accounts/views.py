from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView

from accounts.models import Account, Transaction


class SummaryView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_set = Account.objects.filter(user=self.request.user)
        context["accounts"] = {
            "checking": query_set.filter(type="ch"),
            "savings": query_set.filter(type="sa"),
            "credit": query_set.filter(type="cr"),
            "loan": query_set.filter(type="ln"),
        }
        context["transactions"] = Transaction.objects.filter(account__user=self.request.user).order_by("-created_at")[:5]
        return context


class AccountDetailView(LoginRequiredMixin, DetailView):
    template_name = "accounts/account_detail.html"
    context_object_name = "account"

    def get_object(self, queryset=None):
        return Account.objects.get(uuid=self.kwargs.get("uuid"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO: paginate transactions and use htmx to load more
        # TODO: enable getting transaction by year-month
        context["transactions"] = Transaction.objects.filter(account=self.object)
        return context


class TransactionDetailView(LoginRequiredMixin, DetailView):
    template_name = "accounts/transaction_detail.html"
    context_object_name = "transaction"

    def get_object(self, queryset=None):
        return Transaction.objects.get(uuid=self.kwargs.get("uuid"))


class TransferView(TemplateView):
    pass
