from rest_framework import generics, permissions, status
from rest_framework.response import Response

from core.permissions import IsAdminOrReadOnly, IsVerifiedUser

from .models import InvestmentPlan, UserInvestment
from .serializers import InvestCreateSerializer, InvestmentPlanSerializer, UserInvestmentSerializer
from .services import InvestmentService


class InvestmentPlanListView(generics.ListAPIView):
    """List all active investment plans."""

    serializer_class = InvestmentPlanSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = InvestmentPlan.objects.filter(is_active=True)


class UserInvestmentListView(generics.ListAPIView):
    """List all investments for the authenticated user."""

    serializer_class = UserInvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserInvestment.objects.filter(user=self.request.user)


class UserInvestmentDetailView(generics.RetrieveAPIView):
    """Retrieve a single investment by ID."""

    serializer_class = UserInvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserInvestment.objects.filter(user=self.request.user)


class InvestCreateView(generics.CreateAPIView):
    """Create a new investment (subscribe to a plan)."""

    serializer_class = InvestCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        investment = InvestmentService.create_investment(
            user=request.user,
            plan_id=serializer.validated_data["plan_id"],
            wallet_id=serializer.validated_data["wallet_id"],
            amount=serializer.validated_data["amount"],
        )

        return Response(
            {
                "success": True,
                "message": "Investment created successfully.",
                "data": UserInvestmentSerializer(investment).data,
            },
            status=status.HTTP_201_CREATED,
        )
