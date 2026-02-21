# Telegram online-shop bot template (aiogram 3)

Готовый шаблон Telegram-бота онлайн-магазина на **Python + aiogram 3 + SQLite**.

## Функции
- `/start` и главное меню: Каталог, Корзина, FAQ, Оставить заказ, Связаться.
- Каталог: категории → товары → карточка товара.
- Корзина: добавление, изменение количества (+/-), удаление, очистка, итог.
- Оформление заказа: имя, телефон (с валидацией), адрес, комментарий.
- Сохранение заказа в БД и уведомление админов.
- Админка (по `ADMIN_IDS`):
  - категории (добавить / переименовать / удалить),
  - товары (добавить / редактировать / удалить / in_stock),
  - просмотр последних 10 заказов,
  - кнопки в уведомлении о заказе: "Связаться" и "Пометить обработан".

## Структура
```text
.
├── README.md
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── requirements.txt
├── src/
│   ├── main.py
│   ├── config.py
│   ├── logger.py
│   ├── db/
│   │   ├── models.py
│   │   ├── repo.py
│   │   └── migrate.py
│   ├── bot/
│   │   ├── router.py
│   │   ├── middlewares.py
│   │   ├── states.py
│   │   ├── keyboards.py
│   │   ├── texts.py
│   │   └── handlers/
│   │       ├── start.py
│   │       ├── catalog.py
│   │       ├── cart.py
│   │       ├── order.py
│   │       ├── admin.py
│   │       └── faq.py
│   ├── services/
│   │   ├── catalog_service.py
│   │   ├── order_service.py
│   │   └── notify_service.py
│   └── utils/
│       ├── validators.py
│       ├── time.py
│       └── security.py
├── assets/
│   └── screenshots/
└── tests/
    └── test_smoke.py
```

## Быстрый запуск (локально)
1. Скопируйте env:
   ```bash
   cp .env.example .env
   ```
2. Заполните `.env`:
   - `BOT_TOKEN`
   - `ADMIN_IDS` (через запятую)
   - `DB_PATH` (например `data/shop_bot.db`)
3. Установите зависимости и запустите:
   ```bash
   pip install -r requirements.txt
   python -m src.main
   ```

## Запуск через Docker
```bash
docker compose up -d --build
```

## Конфигурация
Переменные окружения:
- `BOT_TOKEN` — токен Telegram-бота.
- `ADMIN_IDS` — список Telegram user id админов через запятую.
- `DB_PATH` — путь до SQLite файла.

## Как расширять
- Подключить PostgreSQL вместо SQLite.
- Добавить платежные интеграции.
- Добавить промокоды/скидки и историю заказов пользователя.
- Подключить webhook вместо long polling.
