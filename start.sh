#!/usr/bin/env sh
set -eu

TARGET="${APP_TARGET:-backend}"

echo "[start] APP_TARGET=${TARGET}"

if [ "$TARGET" = "backend" ]; then
  cd backend
  alembic upgrade head
  if [ "${RUN_SEED:-false}" = "true" ]; then
    python -m app.seed
  fi
  exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
fi

if [ "$TARGET" = "frontend" ]; then
  cd frontend
  exec npm run start -- -p "${PORT:-3000}"
fi

echo "Unknown APP_TARGET: $TARGET. Use backend or frontend" >&2
exit 1
