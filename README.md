# Wallet Service

Wallet Service — это REST API приложение для управления кошельками.  
Проект реализован с использованием **Django REST Framework** и **PostgreSQL**, упакован в контейнеры с помощью **Docker Compose**.  

---

## Стек технологий
- Python 3.13
- Django 5
- Django REST Framework
- PostgreSQL 15
- Docker / Docker Compose
- Pytest

---

## Запуск проекта

### 1. Клонировать репозиторий
```bash
git clone https://github.com/alex-itx/wallet_app.git
cd wallet_app
```

### 2. Собрать и запустить контейнеры
```bash
docker compose up --build
```

Контейнеры:
- `web` — Django-приложение (http://127.0.0.1:8000)
- `db` — PostgreSQL база данных

### 3. Применить миграции и создать суперпользователя
```bash
docker compose run web python manage.py migrate
docker compose run web python manage.py createsuperuser
```

---

## Переменные окружения

По умолчанию используются значения, заданные в `docker-compose.yml`:

| Переменная       | Значение по умолчанию | Описание                   |
|------------------|-----------------------|----------------------------|
| `DB_NAME`        | wallet_db             | Имя базы данных            |
| `DB_USER`        | wallet_user           | Пользователь БД            |
| `DB_PASSWORD`    | wallet_password       | Пароль БД                  |
| `DB_HOST`        | db                    | Хост базы данных (сервис)  |
| `DB_PORT`        | 5432                  | Порт базы данных           |

---

## API эндпоинты

### Получение баланса кошелька
```
GET /api/v1/wallets/<uuid>/
```

**Пример ответа**
```json
{
  "id": "1a2b3c4d-1234-5678-9012-abcdefabcdef",
  "balance": 1000
}
```

---

### Выполнение операции (пополнение/снятие)
```
POST /api/v1/wallets/<uuid>/operation/
```

**Тело запроса**
```json
{
  "operation_type": "DEPOSIT",  // или "WITHDRAW"
  "amount": 500
}
```

**Пример ответа**
```json
{
  "id": "1a2b3c4d-1234-5678-9012-abcdefabcdef",
  "balance": 1500
}
```

**Пример ошибки**
```json
{
  "detail": "Недостаточно средств"
}
```

---

## Тесты

Запуск тестов внутри контейнера:
```bash
docker compose run web pytest -v
```

Тесты покрывают:
- Получение баланса кошелька
- Пополнение (DEPOSIT)
- Снятие средств (WITHDRAW)
- Ошибку при недостатке средств

---

## Структура проекта

```
wallet_app/
├── wallets/                # Приложение "кошельки"
│   ├── models.py           # Модели (Wallet)
│   ├── serializers.py      # Сериализаторы
│   ├── views.py            # Вьюхи (API)
│   ├── urls.py             # Маршруты приложения
│   └── tests/              # Тесты (pytest)
│
├── wallet_app/             # Django-проект
│   ├── settings.py         # Настройки
│   ├── urls.py             # Главный роутер
│   └── wsgi.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## Особенности реализации

- Баланс хранится в **целых числах** (например, копейках), чтобы избежать ошибок округления при работе с float/decimal.  
- Операции выполняются внутри транзакции с использованием **`select_for_update`** и **`F()`-выражений**, чтобы гарантировать корректность при параллельных запросах.  
- В Docker Compose используется healthcheck для Postgres, чтобы миграции запускались только после готовности базы.  
