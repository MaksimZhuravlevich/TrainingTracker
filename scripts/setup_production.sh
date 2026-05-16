#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python manage.py migrate --noinput
python manage.py collectstatic --noinput
echo "Production setup complete."
