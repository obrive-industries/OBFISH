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

# 1. Pull latest code from GitHub (auto-detect ob-fish, obrive, or origin)
TARGET_REMOTE="origin"
if git remote -v | grep -qE "ob-fish|OBFISH"; then
  TARGET_REMOTE=$(git remote -v | grep -E "ob-fish|OBFISH" | head -n1 | awk '{print $1}')
elif git remote get-url origin 2>/dev/null | grep -q "666ghj/MiroFish"; then
  echo "[!] Detected upstream MiroFish repository in origin. Updating origin to Obrive repo..."
  git remote set-url origin https://github.com/obrive-industries/OBFISH.git || true
  TARGET_REMOTE="origin"
fi

echo "[1/4] Pulling latest production code from remote '$TARGET_REMOTE' branch 'main'..."
git fetch "$TARGET_REMOTE" main
git checkout main
git reset --hard "$TARGET_REMOTE/main"

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
$COMPOSE_CMD build --no-cache
$COMPOSE_CMD up -d

# 5. Check container health & status
echo "[4/4] Verifying container status..."
sleep 5
$COMPOSE_CMD ps

echo "=========================================================="
echo " Synchronizing Admin Credentials inside Container...      "
$COMPOSE_CMD exec -T mirofish uv --directory backend run python scripts/reset_admin.py || true
echo "=========================================================="
echo " Recent Container Logs:                                   "
$COMPOSE_CMD logs --tail 25
echo "=========================================================="
echo "✅ Docker Re-deployment Complete!"
echo "Live URL: https://brain.obrive.com"
echo "=========================================================="
