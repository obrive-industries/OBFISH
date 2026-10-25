#!/usr/bin/env bash
# ==============================================================================
# Brain (Obrive) - Docker Redeploy Script for Hostinger VPS
# ==============================================================================

set -euo pipefail

# Require sudo / root
if [ "$EUID" -ne 0 ]; then
  echo "[-] Please run this script with sudo or as root:"
  echo "    sudo bash deploy/redeploy_docker.sh"
  exit 1
fi

# Detect project directory
if [ -d "/var/www/obmind" ]; then
  APP_DIR="/var/www/obmind"
elif [ -d "/var/www/ob-fish" ]; then
  APP_DIR="/var/www/ob-fish"
else
  APP_DIR="$(pwd)"
fi

echo "=========================================================="
echo " Redeploying Brain via Docker on Hostinger VPS            "
echo " Directory: $APP_DIR                                      "
echo "=========================================================="

cd "$APP_DIR"

# 1. Pull latest code from GitHub
echo "[1/4] Pulling latest production code from GitHub..."
git fetch origin main
git checkout main
git reset --hard origin/main

# 2. Ensure persistent volume directories exist with write permissions
echo "[2/4] Setting up persistent volumes..."
mkdir -p "$APP_DIR/instance" "$APP_DIR/backend/uploads"
chmod -R 777 "$APP_DIR/instance" "$APP_DIR/backend/uploads"

# 3. Detect Docker Compose command
if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  COMPOSE_CMD="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_CMD="docker-compose"
else
  echo "[-] Docker Compose not found on this system!"
  exit 1
fi

# 4. Rebuild image and restart container
echo "[3/4] Rebuilding Docker image and launching container..."
$COMPOSE_CMD down || true
$COMPOSE_CMD build
$COMPOSE_CMD up -d

# 5. Check container health & status
echo "[4/4] Verifying container status..."
sleep 5
$COMPOSE_CMD ps

echo "=========================================================="
echo " Synchronizing Admin Credentials inside Container...      "
$COMPOSE_CMD exec -T mirofish uv run python backend/scripts/reset_admin.py || true
echo "=========================================================="
echo " Recent Container Logs:                                   "
$COMPOSE_CMD logs --tail 25
echo "=========================================================="
echo "✅ Docker Re-deployment Complete!"
echo "Live URL: https://brain.obrive.com"
echo "=========================================================="
