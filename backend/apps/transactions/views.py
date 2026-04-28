from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionListView(generics.ListAPIView):
    """List all transactions for the authenticated user, with optional type filter."""

    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["tx_type"]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
