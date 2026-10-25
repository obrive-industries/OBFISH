#!/usr/bin/env bash
# ==============================================================================
# Script to create or reset the admin user inside the MiroFish Docker container
# Usage: ./set_admin.sh [email] [password]
# ==============================================================================

set -e

EMAIL="${1:-ai@obrive.com}"
PASSWORD="${2:-Yashveer@2910}"

echo "Configuring administrator account: $EMAIL"

# Ensure target directory exists inside the container and copy script
docker compose exec -T mirofish mkdir -p /app/backend/scripts 2>/dev/null || true
docker cp backend/scripts/create_or_reset_admin.py mirofish:/app/backend/scripts/create_or_reset_admin.py 2>/dev/null || true

# Run the admin creator inside the container using the backend virtual environment
if ! docker compose exec -T mirofish uv run --directory backend python scripts/create_or_reset_admin.py "$EMAIL" "$PASSWORD" "Obrive Admin"; then
    echo "Falling back to direct virtualenv python..."
    docker compose exec -T mirofish /app/backend/.venv/bin/python /app/backend/scripts/create_or_reset_admin.py "$EMAIL" "$PASSWORD" "Obrive Admin"
fi
