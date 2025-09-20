import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from wallets.models import Wallet


@pytest.fixture
def api_client():
    """Фикстура для клиента API (аналог self.client у Django TestCase)."""
    return APIClient()


@pytest.fixture
def wallet():
    """Фикстура для создания тестового кошелька."""
    return Wallet.objects.create(balance=1000)


@pytest.mark.django_db
def test_get_wallet_balance(api_client, wallet):
    """Проверка получения баланса кошелька."""
    url = reverse("wallet-detail", args=[wallet.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["balance"] == 1000


@pytest.mark.django_db
def test_deposit_operation(api_client, wallet):
    """Проверка пополнения баланса."""
    url = reverse("wallet-operation", args=[wallet.id])
    data = {"operation_type": "DEPOSIT", "amount": 500}
    response = api_client.post(url, data, format="json")

    wallet.refresh_from_db()

    assert response.status_code == 200
    assert wallet.balance == 1500


@pytest.mark.django_db
def test_withdraw_operation(api_client, wallet):
    """Проверка снятия средств."""
    url = reverse("wallet-operation", args=[wallet.id])
    data = {"operation_type": "WITHDRAW", "amount": 400}
    response = api_client.post(url, data, format="json")

    wallet.refresh_from_db()

    assert response.status_code == 200
    assert wallet.balance == 600


@pytest.mark.django_db
def test_withdraw_not_enough_funds(api_client, wallet):
    """Проверка ошибки при попытке снять больше, чем есть на балансе."""
    url = reverse("wallet-operation", args=[wallet.id])
    data = {"operation_type": "WITHDRAW", "amount": 5000}
    response = api_client.post(url, data, format="json")

    assert response.status_code == 400
    assert response.data["detail"] == "Недостаточно средств"
