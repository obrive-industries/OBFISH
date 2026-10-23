# Brain (Obrive) - Hostinger VPS Deployment Guide

Ye guide step-by-step batati hai ki **Brain** (`brain.obrive.com`, formerly `obmind.obrive.com`) ko Hostinger VPS (Ubuntu 22.04 / 24.04) par kaise deploy karna hai.

---

## 1. Domain & DNS Setup (Hostinger DNS Zone)

Pehle `obrive.com` ke DNS Management (Hostinger Panel) me jaakar ek naya **A Record** add karein:

| Type | Name / Host | Points to (Value) | TTL |
| :--- | :--- | :--- | :--- |
| **A** | `brain` | `<Your_Hostinger_VPS_Public_IP>` | `300` (ya 1/2 Hour) |

> [!NOTE]
> DNS propagate hone me 5 se 15 minute lagte hain. Aap apne local terminal se check kar sakte hain:
> ```bash
> ping brain.obrive.com
> ```
> Jab VPS ki IP ping hone lage, tab aage badhein.

---

## 2. Hostinger Database Setup

ObMind dono MySQL aur PostgreSQL support karta hai. Aap inme se koi ek option choose kar sakte hain:

### Option A: Hostinger Cloud MySQL (Remote Database)
1. Hostinger cPanel / hPanel me **Databases** -> **MySQL Databases** me jayein.
2. Naya database aur user create karein (e.g. `u123456_obmind`, user `u123456_obmind_user`).
3. **Remote MySQL** tab me jaakar apne VPS ki Public IP ko allow karein.
4. `.env` me connection string format:
   ```env
   DATABASE_URL=mysql+pymysql://u123456_obmind_user:YourStrongPassword@sql.hostinger.com:3306/u123456_obmind?charset=utf8mb4
   ```

### Option B: VPS Local PostgreSQL (Recommended for Speed & Isolation)
Agar VPS pe hi PostgreSQL run karna ho:
```bash
sudo apt install -y postgresql postgresql-contrib
sudo -u postgres psql -c "CREATE USER obmind_user WITH PASSWORD 'YourSecurePassword!';"
sudo -u postgres psql -c "CREATE DATABASE obmind_prod OWNER obmind_user;"
```
`.env` me connection string:
```env
DATABASE_URL=postgresql+psycopg2://obmind_user:YourSecurePassword!@127.0.0.1:5432/obmind_prod
```

### Option C: File-based SQLite (Simplest, Zero Setup)
```env
DATABASE_URL=sqlite:////var/www/obmind/instance/obmind_users.db
```

---

## 3. Environment Variables Configuration (`.env`)

Server par `/var/www/obmind/.env` create karein:

```env
# Application Base URL (Verification & Reset email links ke liye)
APP_BASE_URL=https://brain.obrive.com

# JWT Authentication
JWT_SECRET_KEY=generate_a_random_64_char_string_here_with_openssl_rand_hex_32

# Production Database (Hostinger MySQL or PostgreSQL or SQLite)
DATABASE_URL=mysql+pymysql://user:pass@host:3306/db?charset=utf8mb4

# Brevo SMTP Configuration
SMTP_HOST=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USER=bea186001@smtp-brevo.com
SMTP_PASS=your-brevo-smtp-key
SMTP_FROM_EMAIL=ai@obrive.com
SMTP_FROM_NAME=Brain

# Default Platform LLM (Fallback if user does not provide custom BYOK key)
LLM_API_KEY=your-default-llm-key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL_NAME=gpt-4o-mini

# Zep Knowledge Graph Cloud
ZEP_API_KEY=your-zep-api-key
```

---

## 4. Automated 1-Click Deployment Script

VPS me SSH login karein aur repository clone karein:

```bash
# 1. Clone repository
sudo mkdir -p /var/www/obmind
sudo chown -R $USER:$USER /var/www/obmind
git clone https://github.com/your-org/ObMind.git /var/www/obmind

# 2. Setup your .env file
cp /var/www/obmind/.env.example /var/www/obmind/.env
nano /var/www/obmind/.env
# (Save your credentials in .env: Ctrl+O, Enter, Ctrl+X)

# 3. Run automated setup script
cd /var/www/obmind
sudo bash deploy/setup_hostinger.sh
```

Ye script automatically:
1. Python 3.12, Node.js 20, Nginx, Certbot aur system libraries install karegi.
2. Python virtual environment banakar saare dependencies (`Flask`, `SQLAlchemy`, `PyMySQL`, `psycopg2`, `Gunicorn`, etc.) install karegi.
3. Frontend Vue 3 app build karke `/var/www/obmind/frontend/dist` me compile karegi.
4. Systemd service (`obmind.service`) setup karegi jo auto-restart ke saath 4 threaded workers chalata hai.
5. Nginx reverse proxy configure karegi with SSE buffering disabled (simulation streaming ke liye zaroori).
6. Let's Encrypt SSL certificate issue karegi (`https://brain.obrive.com`).
7. UFW firewall enable karegi.

---

## 5. Service Management Commands

Agar kabhi backend restart ya status check karna ho:

```bash
# Check Backend Status
sudo systemctl status obmind

# Restart Backend
sudo systemctl restart obmind

# View Live Logs
sudo journalctl -u obmind -f
# Ya log files dekhein:
tail -f /var/log/obmind/error.log
tail -f /var/log/obmind/access.log

# Check Nginx Status & Reload
sudo nginx -t
sudo systemctl reload nginx
```

---

## 6. How Customer Flow Works

1. Customer visits `https://brain.obrive.com`.
2. Customer clicks **Sign Up** -> Enters Name, Email, Password.
3. Brevo SMTP sends branded HTML verification link: `https://brain.obrive.com/verify-email?token=...`.
4. Customer verifies email -> Verification badge unlocks simulation & ontology builder features.
5. Customer can optionally open **Profile Modal** -> **BYOK (Bring Your Own Key)** section to enter their own OpenAI / Claude / DeepSeek API key.
6. The entire agent swarm and OASIS engine runs using their custom key without any server credit consumption!
