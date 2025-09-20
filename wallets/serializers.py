from rest_framework import serializers
from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения кошелька.
    Используется для GET-запросов (получение информации о балансе).
    """

    class Meta:
        model = Wallet
        fields = ["id", "balance"]


class WalletOperationSerializer(serializers.Serializer):
    """
    Сериализатор для обработки операций пополнения/снятия.
    Используется в POST-запросах на /operation/.
    """

    OPERATION_CHOICES = (
        ("DEPOSIT", "Deposit"),
        ("WITHDRAW", "Withdraw"),
    )

    operation_type = serializers.ChoiceField(
        choices=OPERATION_CHOICES,
        help_text="Тип операции: DEPOSIT (пополнение) или WITHDRAW (снятие)."
    )
    amount = serializers.IntegerField(
        min_value=1,
        help_text="Сумма операции (в минимальных единицах, например копейках)."
    )
