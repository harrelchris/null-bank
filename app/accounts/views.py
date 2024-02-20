from django.views.generic import DetailView, TemplateView

from accounts.models import Account, Transaction


class SummaryView(TemplateView):
    template_name = "accounts/summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["accounts"] = Account.objects.filter(user=self.request.user)
        return context


class AccountDetailView(DetailView):
    template_name = "accounts/account_detail.html"
    context_object_name = "account"

    def get_object(self, queryset=None):
        return Account.objects.get(uuid=self.kwargs.get("uuid"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["transactions"] = Transaction.objects.filter(account=self.object)
        return context


class TransactionDetailView(DetailView):
    template_name = "accounts/transaction_detail.html"
    context_object_name = "transaction"

    def get_object(self, queryset=None):
        return Transaction.objects.get(uuid=self.kwargs.get("uuid"))
