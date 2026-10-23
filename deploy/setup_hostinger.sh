#!/usr/bin/env bash
# ==============================================================================
# ObMind (Obrive) Production Setup Script for Hostinger VPS (Ubuntu/Debian)
# Domain: brain.obrive.com
# ==============================================================================

set -euo pipefail

DOMAIN="brain.obrive.com"
APP_DIR="/var/www/obmind"
LOG_DIR="/var/log/obmind"
SERVICE_NAME="obmind"

echo "=========================================================="
echo " Starting Brain Production Deployment on Hostinger VPS    "
echo " Target Domain: $DOMAIN                                   "
echo " Installation Directory: $APP_DIR                        "
echo "=========================================================="

# 1. Require Root / Sudo
if [ "$EUID" -ne 0 ]; then
  echo "[-] Please run this script with sudo or as root:"
  echo "    sudo bash deploy/setup_hostinger.sh"
  exit 1
fi

# 2. Update System Packages
echo "[1/7] Updating apt repositories and installing core packages..."
apt-get update -y
apt-get install -y \
  python3 \
  python3-pip \
  python3-venv \
  python3-dev \
  build-essential \
  libssl-dev \
  libffi-dev \
  libpq-dev \
  default-libmysqlclient-dev \
  nginx \
  certbot \
  python3-certbot-nginx \
  git \
  curl \
  ufw

# Install Node.js (v20 LTS) if not installed
if ! command -v node >/dev/null 2>&1; then
  echo "[+] Installing Node.js 20 LTS..."
  curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
  apt-get install -y nodejs
fi

# 3. Create Required System Directories and Permissions
echo "[2/7] Creating application directories and log folders..."
mkdir -p "$APP_DIR"
mkdir -p "$LOG_DIR"
mkdir -p "/var/www/certbot"
chown -R www-data:www-data "$LOG_DIR"
chmod 755 "$LOG_DIR"

# 4. Copy Codebase to /var/www/obmind (if script is run from repo directory)
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [ "$CURRENT_DIR" != "$APP_DIR" ]; then
  echo "[3/7] Syncing codebase from $CURRENT_DIR to $APP_DIR..."
  rsync -av --exclude='.git' --exclude='backend/.venv' --exclude='node_modules' "$CURRENT_DIR/" "$APP_DIR/"
fi

# 5. Setup Python Virtual Environment and Backend
echo "[4/7] Setting up Python virtual environment..."
cd "$APP_DIR/backend"
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

# Upgrade pip and install wheels
"$APP_DIR/backend/.venv/bin/pip" install --upgrade pip setuptools wheel
"$APP_DIR/backend/.venv/bin/pip" install -r "$APP_DIR/backend/requirements.txt"

# 6. Build Frontend Static Assets
echo "[5/7] Building frontend production bundle..."
cd "$APP_DIR/frontend"
npm install --production=false
npm run build

# Ensure correct permissions for Nginx and Gunicorn
chown -R www-data:www-data "$APP_DIR"
chmod -R 755 "$APP_DIR"

# Ensure .env exists
if [ ! -f "$APP_DIR/.env" ]; then
  if [ -f "$APP_DIR/.env.example" ]; then
    echo "[!] No .env found. Copying .env.example to .env..."
    cp "$APP_DIR/.env.example" "$APP_DIR/.env"
    echo "[!] IMPORTANT: Edit $APP_DIR/.env with your production database, Brevo SMTP credentials, and LLM API keys!"
  fi
fi

# Ensure instance directory for SQLite fallback has write permissions
mkdir -p "$APP_DIR/instance"
chown -R www-data:www-data "$APP_DIR/instance"
chmod 775 "$APP_DIR/instance"

# 7. Setup Systemd Service
echo "[6/7] Configuring Systemd service ($SERVICE_NAME)..."
cp "$APP_DIR/deploy/systemd/obmind.service" /etc/systemd/system/obmind.service
systemctl daemon-reload
systemctl enable obmind
systemctl restart obmind

# 8. Setup Nginx and SSL
echo "[7/7] Configuring Nginx reverse proxy..."
cp "$APP_DIR/deploy/nginx/brain.obrive.com.conf" /etc/nginx/sites-available/brain.obrive.com.conf

# Clean up legacy site configs if they exist
if [ -f /etc/nginx/sites-enabled/obmind.obrive.com.conf ]; then
  rm -f /etc/nginx/sites-enabled/obmind.obrive.com.conf
fi

# Create symlink if not already present
if [ ! -f /etc/nginx/sites-enabled/brain.obrive.com.conf ]; then
  ln -s /etc/nginx/sites-available/brain.obrive.com.conf /etc/nginx/sites-enabled/
fi

# Remove default site if present
if [ -f /etc/nginx/sites-enabled/default ]; then
  rm -f /etc/nginx/sites-enabled/default
fi

# Test Nginx syntax
nginx -t

# Check if SSL certificate exists, otherwise run Certbot
if [ ! -d "/etc/letsencrypt/live/$DOMAIN" ]; then
  echo "[+] Requesting Let's Encrypt SSL certificate for $DOMAIN..."
  echo "[!] Ensure DNS A-record for $DOMAIN points to this server's public IP before proceeding."
  certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos -m "ai@obrive.com" --redirect || {
    echo "[-] Certbot failed or DNS is not pointing yet. Starting Nginx on HTTP for now..."
  }
fi

systemctl restart nginx

# 9. Configure UFW Firewall
echo "[+] Configuring UFW Firewall (allowing SSH, HTTP, HTTPS)..."
ufw allow 'OpenSSH' || true
ufw allow 'Nginx Full' || true
ufw --force enable || true

echo "=========================================================="
echo " ObMind (Obrive) Deployment Finished Successfully!        "
echo " Service Status: systemctl status obmind                  "
echo " Nginx Logs:     tail -f /var/log/nginx/error.log         "
echo " ObMind Logs:    tail -f /var/log/obmind/error.log        "
echo " Live URL:       https://$DOMAIN                          "
echo "=========================================================="
