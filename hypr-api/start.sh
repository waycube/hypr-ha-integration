#!/usr/bin/env bash

pkill -f "hypr-api.py" >/dev/null 2>&1

cd ~/.local/bin/hypr-api || exit 1

exec uvicorn hypr-api:app \
  --host 127.0.0.1 \
  --port 8129 \
  --log-level warning
