# MVP: Еженедельный операционный контроль ресторанов

Рабочий MVP веб-сервиса для цикла:
**Ресторан → Неделя → Блоки контроля → Задачи → Проблемы → Разбор причин → Решение → Результат**.

## Технологии
- **Frontend:** Next.js 14, TypeScript, Tailwind CSS, App Router
- **Backend:** FastAPI, SQLAlchemy, Pydantic, Alembic, Uvicorn
- **DB:** PostgreSQL
- **Infra:** Docker + docker-compose, подготовлено под Timeweb App Platform

## Структура проекта
```text
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   ├── alembic/
│   ├── Dockerfile
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── Dockerfile
│   └── .env.example
├── docker-compose.yml
└── .env.example
```

## Возможности MVP
- JWT-аутентификация и роли: `admin`, `owner`, `accountant`, `manager`, `chef`
- CRUD по периодам, блокам, задачам, проблемам, метрикам, ценам
- Автосоздание блоков при создании недели
- Автогенерация проблем по метрикам и росту цен поставщиков
- Валидация закрытия проблемы и периода по бизнес-правилам
- Dashboard по ресторанам: red issues, open tasks, revenue, food cost %, fot %

## Seed-данные
Создаются автоматически при старте backend:
- Пользователи:
  - admin@example.com / password123
  - owner@example.com / password123
  - accountant@example.com / password123
  - manager@example.com / password123
  - chef@example.com / password123
- Компания: **KLEVO Group**
- Рестораны: **Клёво Ростов**, **Клёво Сочи**, **Клёво Авиапарк**
- Продукты: Лосось, Тунец, Креветка, Томаты, Авокадо
- Поставщики: FishPro, AgroTrade, PrimeFood
- Примеры недель, метрик, проблем, задач, анализов и комментариев

## Локальный запуск
1. Скопируйте env:
```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```
2. Поднимите проект:
```bash
docker compose up --build
```

## Ключевые команды
- Запуск backend локально:
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload --port 8000
```
- Запуск frontend локально:
```bash
cd frontend
npm install
npm run dev
```

## Swagger
После запуска backend:
- http://localhost:8000/docs
- http://localhost:8000/redoc

## Примеры `.env`
### backend/.env
```env
APP_ENV=development
DATABASE_URL=postgresql+psycopg://ops_user:ops_password@localhost:5432/ops_director
JWT_SECRET=change_this_secret
BACKEND_CORS_ORIGINS=http://localhost:3000
```

### frontend/.env
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Деплой на Timeweb App Platform
1. Запушьте репозиторий в GitHub.
2. В Timeweb создайте приложение типа **Docker Compose**.
3. Укажите путь к `docker-compose.yml` в корне.
4. Добавьте env-переменные из `.env.example` в UI Timeweb.
5. Нажмите Deploy.
6. После деплоя проверьте:
   - `GET /health`
   - `GET /docs`
   - вход в frontend `/login`

## Роуты API
- Auth: `/auth/register`, `/auth/login`, `/auth/me`
- Users: `/users`, `/users/{id}`
- Restaurants: `/restaurants`, `/restaurants/{id}`
- Periods: `/periods`, `/periods/{id}`, `/periods/{id}/blocks`, `/periods/{id}/issues`
- Tasks: `/tasks`, `/tasks/{id}`
- Issues: `/issues`, `/issues/{id}`, `/issues/{id}/analysis`
- Comments: `/comments`, `/issues/{id}/comments`, `/tasks/{id}/comments`
- Metrics: `/metrics`, `/periods/{id}/metrics`, `/metrics/{id}`
- Products/Suppliers/Prices: `/products`, `/suppliers`, `/prices`
- Dashboard: `/dashboard/summary`
