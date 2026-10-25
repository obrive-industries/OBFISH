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

# Run the admin creator inside the container
docker compose exec -T mirofish uv run python backend/scripts/create_or_reset_admin.py "$EMAIL" "$PASSWORD" "Obrive Admin"
