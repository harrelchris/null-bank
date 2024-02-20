from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path(route="", view=views.SummaryView.as_view(), name="summary"),
    path(route="a/<uuid>/", view=views.AccountDetailView.as_view(), name="account_detail"),
    path(route="t/<uuid>/", view=views.TransactionDetailView.as_view(), name="transaction_detail"),
]
