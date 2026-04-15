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
- `POST /api/auth/login`
- `GET /api/auth/me`

## Демо-данные
При старте backend запускается `python -m app.seed` и наполняет БД реалистичными данными:
1. Москва / Авиапарк
2. Ростов-на-Дону
3. Южно-Сахалинск
4. Сочи
5. Санкт-Петербург

`POST /api/demo/reset-data` полностью пересоздает демо-данные.


## Логин и пароль по умолчанию
Если вы не меняли env-переменные в Timeweb:
- Логин: `admin@kapital.director`
- Пароль: `ChangeMeStrongPassword`

Рекомендуется сразу заменить `ADMIN_PASSWORD` и `JWT_SECRET` в переменных окружения.

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
- `BACKEND_INTERNAL_URL`
- `ADMIN_EMAIL`
- `ADMIN_PASSWORD`
- `JWT_SECRET`
- `IIKO_API_LOGIN`
- `IIKO_BASE_URL`

> Важно: в `docker-compose.yml` **не используется `env_file`**. Это сделано специально для Timeweb, где переменные задаются в интерфейсе App Platform.

## Деплой в Timeweb App Platform (из GitHub)
1. Загрузите проект в GitHub-репозиторий.
2. В Timeweb создайте приложение типа **Docker Compose**.
3. Подключите GitHub-репозиторий и выберите ветку.
4. Убедитесь, что в корне есть `docker-compose.yml`, `.env.example`, `README.md`.
5. Добавьте env-переменные из `.env.example` в интерфейсе Timeweb.
6. Нажмите **Deploy**.

> В `docker-compose.yml` сервисы идут в порядке: `frontend` → `backend` → `db`.


## Если была ошибка `.env not found`
Если в логах Timeweb есть ошибка вида:
`env file .../.env not found`
это означает, что в compose использовался `env_file: .env`. В этом проекте `env_file` убран, а все переменные нужно задавать в UI Timeweb.

После обновления репозитория:
1. Откройте приложение в Timeweb.
2. Убедитесь, что все переменные добавлены.
3. Запустите новый Deploy.

## Текущие ограничения
- Авторизация через backend (`POST /api/auth/login`) с логином/паролем из env-переменных.
- Данные синтетические и перезаписываются reset-эндпоинтом.
- Не реализованы RBAC, аудит действий, webhooks и интеграции с ERP/POS.

## Что не нужно запускать локально
Так как деплой идет сразу из GitHub в облако Timeweb, **локально не обязательно** выполнять:
- `docker compose up`
- `npm install`
- `pip install -r requirements.txt`
- любые миграции вручную

Проект стартует в контейнерах на платформе автоматически.



## Интеграция с iikoCloud
Поддержан статус интеграции с iiko:
- `GET /api/integrations/iiko/status`

Для работы задайте в Timeweb env:
- `IIKO_API_LOGIN` — ваш API login iiko (добавляйте только в переменные среды Timeweb, не в код)
- `IIKO_BASE_URL` — по умолчанию `https://api-ru.iiko.services`

После деплоя можно проверить интеграцию запросом к endpoint `GET /api/integrations/iiko/status`.


## Проверка iiko в UI
На странице `/dashboard` выводится статус подключения iiko (подключено/не подключено и количество организаций).


### Где вставлять API ключ (правильно)
Ключ iiko нужно добавлять **в переменные окружения на сервере (Timeweb App Platform)**, а не в репозиторий и не в исходный код.

1. Timeweb → ваше приложение → Environment Variables.
2. Добавьте `IIKO_API_LOGIN=<ваш_ключ>` и при необходимости `IIKO_BASE_URL=https://api-ru.iiko.services`.
3. Нажмите Deploy.
4. Проверьте `GET /api/integrations/iiko/status` — должен вернуть `connected: true`.


### Проверка по официальной схеме Authorization (iiko)
По инструкции iikoCloud сначала получается access token через `POST /api/1/access_token` с телом `{ "apiLogin": "..." }`, затем этот токен используется в запросах API.

Пример проверки на сервере (через наш backend endpoint):
```bash
curl -X GET "https://<ваш-домен>/api/integrations/iiko/status"
```

Прямой пример получения токена из iiko (для диагностики):
```bash
curl -X POST "https://api-ru.iiko.services/api/1/access_token" \
  -H "Content-Type: application/json" \
  -d '{"apiLogin":"<IIKO_API_LOGIN>"}'
```


### Production-авторизация
Логин выполняется через backend endpoint `POST /api/auth/login`.
Учетные данные хранятся в серверных env: `ADMIN_EMAIL`, `ADMIN_PASSWORD`, `JWT_SECRET`.
Frontend не содержит хардкоженных логинов/паролей.


### Если логин пишет "Unable to reach backend auth service"
В проект добавлен fallback в Next API (`/api/auth/login`): если frontend не может достучаться до backend по внутреннему адресу, вход выполняется по `ADMIN_EMAIL`/`ADMIN_PASSWORD` на стороне frontend-сервера.

Это позволяет зайти в интерфейс даже при сетевых ограничениях платформы.


### Как протестировать API из интерфейса
1. Откройте `/api-test` в приложении.
2. Страница вызовет `GET /api/system/backend-check` и покажет, какие backend URL проверены и какие из них доступны.
3. Если все `ok: false`, проверьте env `BACKEND_INTERNAL_URL` и сервис `backend` в Timeweb.
