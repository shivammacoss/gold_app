from rest_framework import generics, permissions

from core.permissions import IsOwner

from .models import Wallet
from .serializers import WalletSerializer
from .services import WalletService


class WalletListView(generics.ListAPIView):
    """List all wallets belonging to the authenticated user."""

    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WalletService.get_user_wallets(self.request.user)


class WalletDetailView(generics.RetrieveAPIView):
    """Retrieve a single wallet by ID."""

    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Wallet.objects.all()
