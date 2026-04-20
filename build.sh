#!/usr/bin/env sh
set -eu

TARGET="${APP_TARGET:-backend}"

echo "[build] APP_TARGET=${TARGET}"

if [ "$TARGET" = "backend" ]; then
  cd backend
  pip install --no-cache-dir -r requirements.txt
  exit 0
fi

if [ "$TARGET" = "frontend" ]; then
  cd frontend
  npm ci
  npm run build
  exit 0
fi

echo "Unknown APP_TARGET: $TARGET. Use backend or frontend" >&2
exit 1
