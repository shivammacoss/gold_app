from django.urls import path

from . import views

app_name = "investments"

urlpatterns = [
    path("plans/", views.InvestmentPlanListView.as_view(), name="plan-list"),
    path("", views.UserInvestmentListView.as_view(), name="investment-list"),
    path("create/", views.InvestCreateView.as_view(), name="investment-create"),
    path("<uuid:pk>/", views.UserInvestmentDetailView.as_view(), name="investment-detail"),
]
