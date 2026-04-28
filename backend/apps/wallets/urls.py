from django.urls import path

from . import views

app_name = "wallets"

urlpatterns = [
    path("", views.WalletListView.as_view(), name="wallet-list"),
    path("<uuid:pk>/", views.WalletDetailView.as_view(), name="wallet-detail"),
]
