from rest_framework import generics, permissions

from .models import Deposit
from .serializers import DepositSerializer


class DepositListView(generics.ListAPIView):
    """List all deposits for the authenticated user."""

    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Deposit.objects.filter(user=self.request.user)


class DepositDetailView(generics.RetrieveAPIView):
    """Retrieve a single deposit by ID."""

    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Deposit.objects.filter(user=self.request.user)
