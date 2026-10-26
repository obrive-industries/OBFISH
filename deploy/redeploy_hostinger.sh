#!/usr/bin/env bash
# ==============================================================================
# Brain (Obrive) Quick Redeployment Script for Hostinger VPS
# Domain: brain.obrive.com / obfish.obrive.com
# ==============================================================================

set -euo pipefail

# Require sudo / root
if [ "$EUID" -ne 0 ]; then
  echo "[-] Please run this script with sudo or as root:"
  echo "    sudo bash deploy/redeploy_hostinger.sh"
  exit 1
fi

# 1. Detect app directory
if [ -d "/var/www/obmind" ]; then
  APP_DIR="/var/www/obmind"
elif [ -d "/var/www/ob-fish" ]; then
  APP_DIR="/var/www/ob-fish"
else
  APP_DIR="$(pwd)"
fi

echo "=========================================================="
echo " Redeploying Brain Changes on Hostinger VPS               "
echo " Working Directory: $APP_DIR                              "
echo "=========================================================="

cd "$APP_DIR"

# 2. Pull latest git changes (auto-detect ob-fish, obrive, or origin)
TARGET_REMOTE="origin"
if git remote -v | grep -qE "ob-fish|OBFISH"; then
  TARGET_REMOTE=$(git remote -v | grep -E "ob-fish|OBFISH" | head -n1 | awk '{print $1}')
elif git remote get-url origin 2>/dev/null | grep -q "666ghj/MiroFish"; then
  echo "[!] Detected upstream MiroFish repository in origin. Updating origin to Obrive repo..."
  git remote set-url origin https://github.com/obrive-industries/OBFISH.git || true
  TARGET_REMOTE="origin"
fi

echo "[1/5] Pulling latest production code from remote '$TARGET_REMOTE' branch 'main'..."
git fetch "$TARGET_REMOTE" main
git checkout main
git reset --hard "$TARGET_REMOTE/main"

# 3. Update backend virtualenv dependencies
echo "[2/5] Updating backend python dependencies..."
if [ -d "$APP_DIR/backend/.venv" ]; then
  "$APP_DIR/backend/.venv/bin/pip" install --upgrade pip
  "$APP_DIR/backend/.venv/bin/pip" install -r "$APP_DIR/backend/requirements.txt"
fi

# 4. Rebuild frontend production assets
echo "[3/5] Re-compiling frontend production build..."
cd "$APP_DIR/frontend"
npm install --production=false
npm run build
cd "$APP_DIR"

# 5. Ensure file ownership & permissions
echo "[4/5] Setting ownership and permissions..."
if id "www-data" >/dev/null 2>&1; then
  WEB_USER="www-data:www-data"
elif id "nginx" >/dev/null 2>&1; then
  WEB_USER="nginx:nginx"
elif id "apache" >/dev/null 2>&1; then
  WEB_USER="apache:apache"
else
  WEB_USER="$(id -un):$(id -gn)"
fi

chown -R "$WEB_USER" "$APP_DIR" || true
chmod -R 755 "$APP_DIR"
mkdir -p "$APP_DIR/instance" "$APP_DIR/backend/uploads"
chown -R "$WEB_USER" "$APP_DIR/instance" "$APP_DIR/backend/uploads" || true
chmod 775 "$APP_DIR/instance" "$APP_DIR/backend/uploads"

# 6. Restart backend service & reload Nginx
echo "[5/5] Restarting services..."
if systemctl list-unit-files | grep -q "obmind.service"; then
  systemctl restart obmind
  echo "[+] Restarted obmind systemd service"
elif [ -f "$APP_DIR/docker-compose.yml" ] && command -v docker >/dev/null 2>&1; then
  docker compose restart
  echo "[+] Restarted docker compose"
elif command -v pm2 >/dev/null 2>&1; then
  pm2 restart all
  echo "[+] Restarted pm2"
fi

systemctl reload nginx
echo "[+] Reloaded Nginx"

echo "=========================================================="
echo " Synchronizing Admin Credentials...                       "
if [ -d "$APP_DIR/backend/.venv" ]; then
  "$APP_DIR/backend/.venv/bin/python" "$APP_DIR/backend/scripts/reset_admin.py" || true
fi

# 7. Smoke test
echo "=========================================================="
echo " Verifying Live Daemon Status...                          "
sleep 2
curl -s -i http://127.0.0.1:5001/api/health || true
echo ""
echo "✅ Brain Redeployment Complete!"
echo "Live URL: https://brain.obrive.com"
echo "=========================================================="
