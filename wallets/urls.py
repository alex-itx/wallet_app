from django.urls import path
from .views import WalletDetailView, WalletOperationView

urlpatterns = [
    path("<uuid:id>/", WalletDetailView.as_view(), name="wallet-detail"),
    path("<uuid:id>/operation/", WalletOperationView.as_view(), name="wallet-operation"),
]
