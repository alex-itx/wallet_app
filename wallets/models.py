import uuid
from django.db import models
from django.utils import timezone


class Wallet(models.Model):
    """
    Модель кошелька.
    Каждый кошелёк имеет уникальный UUID и баланс.
    Баланс будем хранить в целых числах (например, копейках),
    чтобы избежать ошибок округления с float/decimal при деньгах.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text="Уникальный идентификатор кошелька (UUID)."
    )
    balance = models.BigIntegerField(
        default=0,
        help_text="Текущий баланс в минимальных единицах валюты (например, копейках)."
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="Дата и время создания кошелька."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Дата и время последнего изменения кошелька."
    )

    class Meta:
        db_table = "wallets"
        verbose_name = "Кошелёк"
        verbose_name_plural = "Кошельки"

    def __str__(self):
        return f"Wallet {self.id} (balance={self.balance})"
