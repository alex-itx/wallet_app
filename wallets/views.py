from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response

from .models import Wallet
from .serializers import WalletSerializer, WalletOperationSerializer


class WalletDetailView(generics.RetrieveAPIView):
    """
    Эндпоинт для получения информации о кошельке по UUID.
    GET /api/v1/wallets/<uuid>/
    """

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = "id"  # Указываем, что поиск идёт по UUID


class WalletOperationView(generics.GenericAPIView):
    """
    Эндпоинт для выполнения операций с кошельком (пополнение или снятие).
    POST /api/v1/wallets/<uuid>/operation/
    """

    serializer_class = WalletOperationSerializer

    def post(self, request, *args, **kwargs):
        # Получаем объект кошелька или возвращаем 404
        wallet = get_object_or_404(Wallet, id=kwargs.get("id"))

        # Валидируем входные данные
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        operation_type = serializer.validated_data["operation_type"]
        amount = serializer.validated_data["amount"]

        # Оборачиваем в транзакцию для защиты от конкурентных изменений
        with transaction.atomic():
            # Захватываем блокировку строки (FOR UPDATE),
            # чтобы параллельные операции ждали друг друга
            wallet = Wallet.objects.select_for_update().get(id=wallet.id)

            if operation_type == "DEPOSIT":
                # Увеличиваем баланс через F(), чтобы обновление было атомарным
                wallet.balance = F("balance") + amount
                wallet.save(update_fields=["balance"])
            elif operation_type == "WITHDRAW":
                # Проверяем, достаточно ли средств
                if wallet.balance < amount:
                    return Response(
                        {"detail": "Недостаточно средств"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                wallet.balance = F("balance") - amount
                wallet.save(update_fields=["balance"])

        # Перечитываем объект из базы, чтобы получить актуальный баланс
        wallet.refresh_from_db()

        return Response(
            WalletSerializer(wallet).data,
            status=status.HTTP_200_OK
        )
