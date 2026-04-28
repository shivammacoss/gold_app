from django.urls import path

from . import views

app_name = "withdrawals"

urlpatterns = [
    path("", views.WithdrawalListView.as_view(), name="withdrawal-list"),
    path("create/", views.WithdrawalCreateView.as_view(), name="withdrawal-create"),
    path("<uuid:pk>/", views.WithdrawalDetailView.as_view(), name="withdrawal-detail"),
]
