# MVP «Операционный директор сети ресторанов»

Демо SaaS-продукт для инвестора: единая панель управления операционными метриками сети из 5 ресторанов. Проект готов к деплою через **Timeweb App Platform** напрямую из GitHub как Docker Compose приложение.

## Стек
- **Frontend:** Next.js 14, TypeScript, Tailwind CSS, shadcn/ui-style components, lucide-react, Recharts
- **Backend:** FastAPI, Python 3.11, SQLAlchemy, Pydantic, Alembic
- **DB:** PostgreSQL

## Структура проекта
```text
.
├── docker-compose.yml
├── .env.example
├── README.md
├── backend
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── seed.py
│   ├── alembic.ini
│   ├── alembic/
│   └── app/
│       ├── main.py
│       ├── seed.py
│       ├── core/
│       ├── db/
│       ├── models/
│       ├── schemas/
│       ├── api/
│       └── services/
└── frontend
    ├── Dockerfile
    ├── package.json
    ├── app/
    ├── components/
    └── lib/
```

## Что умеет MVP
- Сводные KPI сети: выручка, food/labor cost, списания, прибыль
- Аналитика потерь по категориям и ресторанам
- Контроль закупок и поставщиков: сравнение с рынком и динамика цен
- Мониторинг заготовок и риска перепроизводства
- Контроль эффективности кухонных станций и узких мест
- Таблица рентабельности ресторанов

## Backend API
- `GET /health`
- `GET /api/restaurants`
- `GET /api/restaurants/{id}`
- `GET /api/dashboard/summary`
- `GET /api/dashboard/losses`
- `GET /api/dashboard/suppliers`
- `GET /api/dashboard/prep`
- `GET /api/dashboard/kitchen`
- `GET /api/dashboard/profitability`
- `POST /api/demo/reset-data`

## Демо-данные
При старте backend запускается `python -m app.seed` и наполняет БД реалистичными данными:
1. Москва / Авиапарк
2. Ростов-на-Дону
3. Южно-Сахалинск
4. Сочи
5. Санкт-Петербург

`POST /api/demo/reset-data` полностью пересоздает демо-данные.

## Переменные окружения (Timeweb)
Используйте значения из `.env.example`:
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `DATABASE_URL`
- `BACKEND_CORS_ORIGINS`
- `APP_ENV`
- `NEXT_PUBLIC_API_URL`

## Деплой в Timeweb App Platform (из GitHub)
1. Загрузите проект в GitHub-репозиторий.
2. В Timeweb создайте приложение типа **Docker Compose**.
3. Подключите GitHub-репозиторий и выберите ветку.
4. Убедитесь, что в корне есть `docker-compose.yml`, `.env.example`, `README.md`.
5. Добавьте env-переменные из `.env.example` в интерфейсе Timeweb.
6. Нажмите **Deploy**.

> В `docker-compose.yml` сервисы идут в порядке: `frontend` → `backend` → `db`.

## Ограничения демо-версии
- Авторизация демонстрационная (`/login` без реальной проверки).
- Данные синтетические и перезаписываются reset-эндпоинтом.
- Не реализованы RBAC, аудит действий, webhooks и интеграции с ERP/POS.

## Что не нужно запускать локально
Так как деплой идет сразу из GitHub в облако Timeweb, **локально не обязательно** выполнять:
- `docker compose up`
- `npm install`
- `pip install -r requirements.txt`
- любые миграции вручную

Проект стартует в контейнерах на платформе автоматически.
