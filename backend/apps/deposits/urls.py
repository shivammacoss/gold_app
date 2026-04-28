from django.urls import path

from . import views

app_name = "deposits"

urlpatterns = [
    path("", views.DepositListView.as_view(), name="deposit-list"),
    path("<uuid:pk>/", views.DepositDetailView.as_view(), name="deposit-detail"),
]
