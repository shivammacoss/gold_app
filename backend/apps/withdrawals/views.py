from rest_framework import generics, permissions, status
from rest_framework.response import Response

from core.permissions import IsVerifiedUser

from .models import Withdrawal
from .serializers import WithdrawalCreateSerializer, WithdrawalSerializer
from .services import WithdrawalService


class WithdrawalListView(generics.ListAPIView):
    """List all withdrawals for the authenticated user."""

    serializer_class = WithdrawalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Withdrawal.objects.filter(user=self.request.user)


class WithdrawalCreateView(generics.CreateAPIView):
    """Create a new withdrawal request."""

    serializer_class = WithdrawalCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        withdrawal = WithdrawalService.create_withdrawal(
            user=request.user,
            wallet=serializer.validated_data["wallet"],
            amount=serializer.validated_data["amount"],
            to_address=serializer.validated_data["to_address"],
            network=serializer.validated_data["network"],
        )

        return Response(
            {
                "success": True,
                "message": "Withdrawal request created. Pending admin approval.",
                "data": WithdrawalSerializer(withdrawal).data,
            },
            status=status.HTTP_201_CREATED,
        )


class WithdrawalDetailView(generics.RetrieveAPIView):
    """Retrieve a single withdrawal by ID."""

    serializer_class = WithdrawalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Withdrawal.objects.filter(user=self.request.user)
