# Restaurant Ops Dashboard MVP (iiko email)

## Run
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

## Seed restaurants
```bash
python -m app.seed_iiko
```

## Endpoints
- GET /health
- GET/POST /restaurants
- GET /restaurants/{id}/dashboard
- GET /restaurants/{id}/imports
- POST /imports/manual-upload
- POST /email/check-now
- GET /alerts
- POST /telegram/test-alert/{restaurant_id}

## Fake report generator
Use `backend/sample_reports/generate_fake_reports.py`.
