# MVP: Еженедельный операционный контроль ресторанов

Рабочий MVP веб-сервиса для бухгалтера и операционного контроля ресторанов:
**Ресторан → Неделя → Блоки → Метрики → Проблемы → Разбор причин → Решение → Результат**.

## Стек
- Frontend: Next.js 14+, TypeScript, App Router, Tailwind CSS.
- Backend: FastAPI, SQLAlchemy, Pydantic, Alembic, Uvicorn.
- DB: PostgreSQL.
- Infra: Docker/Docker Compose + Railway deploy config.

## Структура файлов
```text
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── main.py
│   │   └── seed.py
│   ├── alembic/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app/
│   │   ├── dashboard/
│   │   ├── login/
│   │   ├── restaurants/[id]/
│   │   ├── periods/[id]/
│   │   ├── issues/
│   │   ├── tasks/
│   │   └── prices/
│   ├── components/
│   ├── lib/
│   ├── Dockerfile
│   └── .env.example
├── docker-compose.yml
├── .env.example
└── README.md
```

## Что реализовано
- Роли: `admin`, `owner`, `accountant`, `manager`, `chef`.
- Периоды со статусами: `in_progress`, `review`, `issues`, `closed`.
- Автосоздание блоков при создании периода.
- Метрики недели + авто-генерация проблем (issues) по правилам.
- Проблемы и разбор причин (IssueAnalysis), нельзя закрыть issue без `reason + solution + assigned_user_id`.
- Задачи по блокам.
- Закупочные цены и авто issue при росте цены поставщика.
- Запрет закрытия периода при наличии открытых issues/tasks.
- Dashboard для бухгалтера с ключевыми KPI.

## Seed-данные
Создаются через `python -m app.seed`:
- Пользователи:
  - admin@example.com / password123
  - owner@example.com / password123
  - accountant@example.com / password123
  - manager@example.com / password123
  - chef@example.com / password123
- Компания: KLEVO Group.
- Рестораны: Клёво Ростов, Клёво Сочи, Клёво Авиапарк.
- Продукты: Лосось, Тунец, Креветка, Томаты, Авокадо.
- Поставщики: FishPro, AgroTrade, PrimeFood.
- Примерные недели, метрики, задачи, проблемы, анализы.

## Local run
### 1) Подготовка env
```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### 2) Запуск в Docker
```bash
docker compose up --build
```

Приложения:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Swagger: http://localhost:8000/docs

## Миграции
```bash
cd backend
alembic upgrade head
```

## Seed
```bash
cd backend
python -m app.seed
```

## Пример `.env` backend
```env
APP_ENV=development
DATABASE_URL=postgresql+psycopg://ops_user:ops_password@localhost:5432/ops_director
JWT_SECRET=change_this_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
BACKEND_CORS_ORIGINS=http://localhost:3000
```

## Пример `.env` frontend
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Deploy to Railway

### 1) Backend service
1. Создать сервис в Railway, выбрать репозиторий и Root Directory = `backend`.
2. Railway автоматически подхватит `backend/railway.json` и `backend/Dockerfile`.
3. Добавить env:
   - `DATABASE_URL`
   - `JWT_SECRET`
   - `BACKEND_CORS_ORIGINS=https://<frontend-domain>`
   - `RUN_SEED=false` (или `true` только для первичного наполнения)
4. Railway сам подставляет `PORT`, Dockerfile это учитывает.

### 2) Frontend service
1. Создать второй сервис в Railway с Root Directory = `frontend`.
2. Railway использует `frontend/railway.json` и `frontend/Dockerfile`.
3. Добавить env:
   - `NEXT_PUBLIC_API_URL=https://<backend-domain>`
4. Проверить `/login` и `/dashboard`.

### 3) PostgreSQL в Railway
1. В проекте Railway нажать **New → Database → PostgreSQL**.
2. Скопировать `DATABASE_URL` из переменных БД.
3. Прописать этот `DATABASE_URL` в backend service.
4. На первом запуске backend автоматически применит миграции (`alembic upgrade head`).
5. Для тестовых данных временно выставить `RUN_SEED=true`, затем вернуть `false`.

## Основные API
- Auth: `POST /auth/register`, `POST /auth/login`, `GET /auth/me`
- Restaurants: `GET /restaurants`, `POST /restaurants`, `GET /restaurants/{id}`
- Periods: `GET /periods`, `POST /periods`, `GET /periods/{id}`, `PATCH /periods/{id}`
- Blocks: `GET /periods/{period_id}/blocks`
- Metrics: `POST /metrics`, `GET /periods/{period_id}/metrics`, `PATCH /metrics/{id}`
- Issues: `GET /issues`, `GET /issues/{id}`, `GET /periods/{period_id}/issues`, `POST /issues`, `PATCH /issues/{id}`
- Issue analysis: `POST /issues/{id}/analysis`, `PATCH /issues/{id}/analysis`
- Tasks: `GET /tasks`, `POST /tasks`, `GET /tasks/{id}`, `PATCH /tasks/{id}`, `DELETE /tasks/{id}`
- Products: `GET /products`, `POST /products`
- Suppliers: `GET /suppliers`, `POST /suppliers`
- Prices: `GET /prices`, `POST /prices`
- Dashboard: `GET /dashboard/summary`
