"""\n配置管理\n统一从项目根目录的 .env 文件加载配置\n"""

import os
from dotenv import load_dotenv

# 加载项目根目录的 .env 文件
# Path: Brain/.env (relative to backend/app/config.py)
project_root_env = os.path.join(os.path.dirname(__file__), '../../.env')

if os.path.exists(project_root_env):
    load_dotenv(project_root_env, override=True)
else:
    # 如果根目录没有 .env，尝试加载环境变量（用于生产环境）
    load_dotenv(override=True)


class Config:
    """Flask配置类"""
    
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY', 'brain-secret-key')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Database (SQLAlchemy)
    # Default: SQLite for local dev. Set DATABASE_URL to postgres:// or postgresql:// for production.
    _brain_db = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../instance/brain_users.db'))
    _legacy_db = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../instance/obmind_users.db'))
    _default_db = _legacy_db if (not os.path.exists(_brain_db) and os.path.exists(_legacy_db)) else _brain_db
    
    _raw_db_url = os.environ.get('DATABASE_URL')
    if _raw_db_url and _raw_db_url.startswith('postgres://'):
        _raw_db_url = _raw_db_url.replace('postgres://', 'postgresql://', 1)

    if _raw_db_url and 'sqlite' in _raw_db_url:
        _sqlite_file = _raw_db_url.replace('sqlite:///', '')
        try:
            _target_dir = os.path.dirname(os.path.abspath(_sqlite_file))
            os.makedirs(_target_dir, exist_ok=True)
        except Exception:
            _raw_db_url = None

    try:
        os.makedirs(os.path.dirname(_default_db), exist_ok=True)
    except Exception:
        pass

    SQLALCHEMY_DATABASE_URI = _raw_db_url or f'sqlite:///{_default_db}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # JWT
    JWT_ACCESS_TTL_MINUTES = int(os.environ.get('JWT_ACCESS_TTL_MINUTES', '60'))
    JWT_REFRESH_TTL_DAYS = int(os.environ.get('JWT_REFRESH_TTL_DAYS', '30'))

    # Brevo / SMTP Configuration
    SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp-relay.brevo.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
    SMTP_USER = os.environ.get('SMTP_USER', '')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
    SMTP_FROM_NAME = os.environ.get('SMTP_FROM_NAME', 'Brain')
    SMTP_FROM_EMAIL = os.environ.get('SMTP_FROM_EMAIL', 'ai@obrive.com')
    APP_BASE_URL = os.environ.get('APP_BASE_URL', 'https://brain.obrive.com').rstrip('/')

    # LLM配置（统一使用OpenAI格式）
    LLM_API_KEY = os.environ.get('LLM_API_KEY')
    LLM_BASE_URL = os.environ.get('LLM_BASE_URL', 'https://api.openai.com/v1')
    LLM_MODEL_NAME = os.environ.get('LLM_MODEL_NAME', 'gpt-4o-mini')
    ONTOLOGY_MAX_TEXT_LENGTH = int(
        os.environ.get('ONTOLOGY_MAX_TEXT_LENGTH', '30000')
    )
    LLM_BOOST_API_KEY = os.environ.get('LLM_BOOST_API_KEY')
    LLM_BOOST_BASE_URL = os.environ.get('LLM_BOOST_BASE_URL')
    LLM_BOOST_MODEL_NAME = os.environ.get('LLM_BOOST_MODEL_NAME')
    LLM_BACKUP_API_KEY = os.environ.get('LLM_BACKUP_API_KEY')
    LLM_BACKUP_BASE_URL = os.environ.get('LLM_BACKUP_BASE_URL')
    LLM_BACKUP_MODEL_NAME = os.environ.get('LLM_BACKUP_MODEL_NAME')
    LLM_FALLBACK_API_KEY = os.environ.get('LLM_FALLBACK_API_KEY')
    LLM_FALLBACK_BASE_URL = os.environ.get('LLM_FALLBACK_BASE_URL')
    LLM_FALLBACK_MODEL_NAME = os.environ.get('LLM_FALLBACK_MODEL_NAME')
    
    # Zep配置
    ZEP_API_KEY = os.environ.get('ZEP_API_KEY')
    ZEP_BACKUP_API_KEY = os.environ.get('ZEP_BACKUP_API_KEY')
    ZEP_API_KEYS_ENV = os.environ.get('ZEP_API_KEYS')

    # Accounts listed here receive unlimited plan access (comma separated).
    ADMIN_EMAILS_ENV = os.environ.get('ADMIN_EMAILS', '')

    # Razorpay subscription billing (USD plans created by setup_razorpay_plans.py)
    RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID')
    RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET')
    RAZORPAY_WEBHOOK_SECRET = os.environ.get('RAZORPAY_WEBHOOK_SECRET')
    RAZORPAY_PLAN_ID_STARTER_MONTHLY = os.environ.get('RAZORPAY_PLAN_ID_STARTER_MONTHLY')
    RAZORPAY_PLAN_ID_STARTER_ANNUAL = os.environ.get('RAZORPAY_PLAN_ID_STARTER_ANNUAL')
    RAZORPAY_PLAN_ID_PRO_MONTHLY = os.environ.get('RAZORPAY_PLAN_ID_PRO_MONTHLY')
    RAZORPAY_PLAN_ID_PRO_ANNUAL = os.environ.get('RAZORPAY_PLAN_ID_PRO_ANNUAL')
    RAZORPAY_PLAN_ID_PREMIUM_MONTHLY = os.environ.get('RAZORPAY_PLAN_ID_PREMIUM_MONTHLY')
    RAZORPAY_PLAN_ID_PREMIUM_ANNUAL = os.environ.get('RAZORPAY_PLAN_ID_PREMIUM_ANNUAL')

    @classmethod
    def admin_emails(cls) -> set[str]:
        """Return the normalized set of admin email addresses."""

        import re

        return {
            email.strip().lower()
            for email in re.split(r'[,;\s]+', getattr(cls, 'ADMIN_EMAILS_ENV', '') or '')
            if email.strip()
        }

    @classmethod
    def get_llm_api_keys(cls) -> list[str]:
        """返回所有配置的 LLM API Key 列表（去重且保序）"""
        import re
        raw = getattr(cls, 'LLM_API_KEY', '') or ''
        seen = set()
        keys: list[str] = []
        for k in re.split(r'[,;\s]+', str(raw)):
            clean = k.strip().strip("'\"")
            if clean and clean not in seen:
                seen.add(clean)
                keys.append(clean)
        return keys

    @classmethod
    def get_zep_api_keys(cls) -> list[str]:
        """返回所有配置的 Zep API Key 列表（去重且保序）"""
        import re
        raw_candidates = []
        if getattr(cls, 'ZEP_API_KEYS_ENV', None):
            raw_candidates.extend(re.split(r'[,;\s]+', str(cls.ZEP_API_KEYS_ENV)))
        if getattr(cls, 'ZEP_API_KEY', None):
            raw_candidates.extend(re.split(r'[,;\s]+', str(cls.ZEP_API_KEY)))
        if getattr(cls, 'ZEP_BACKUP_API_KEY', None):
            raw_candidates.extend(re.split(r'[,;\s]+', str(cls.ZEP_BACKUP_API_KEY)))
        
        seen = set()
        keys: list[str] = []
        for k in raw_candidates:
            clean = k.strip().strip("'\"")
            if clean and clean not in seen:
                seen.add(clean)
                keys.append(clean)
        return keys
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'md', 'txt', 'markdown', 'docx'}
    
    # 文本处理配置
    DEFAULT_CHUNK_SIZE = 500  # 默认切块大小
    DEFAULT_CHUNK_OVERLAP = 50  # 默认重叠大小
    
    # OASIS模拟配置
    OASIS_DEFAULT_MAX_ROUNDS = int(os.environ.get('OASIS_DEFAULT_MAX_ROUNDS', '10'))
    OASIS_SIMULATION_DATA_DIR = os.path.join(os.path.dirname(__file__), '../uploads/simulations')
    
    # OASIS平台可用动作配置
    OASIS_TWITTER_ACTIONS = [
        'CREATE_POST', 'LIKE_POST', 'REPOST', 'FOLLOW', 'DO_NOTHING', 'QUOTE_POST'
    ]
    OASIS_REDDIT_ACTIONS = [
        'LIKE_POST', 'DISLIKE_POST', 'CREATE_POST', 'CREATE_COMMENT',
        'LIKE_COMMENT', 'DISLIKE_COMMENT', 'SEARCH_POSTS', 'SEARCH_USER',
        'TREND', 'REFRESH', 'DO_NOTHING', 'FOLLOW', 'MUTE'
    ]
    
    # Report Agent配置
    REPORT_AGENT_MAX_TOOL_CALLS = int(os.environ.get('REPORT_AGENT_MAX_TOOL_CALLS', '5'))
    REPORT_AGENT_MAX_REFLECTION_ROUNDS = int(os.environ.get('REPORT_AGENT_MAX_REFLECTION_ROUNDS', '2'))
    REPORT_AGENT_TEMPERATURE = float(os.environ.get('REPORT_AGENT_TEMPERATURE', '0.5'))
    
    @classmethod
    def get_cors_origins(cls) -> list[str]:
        """返回允许跨域访问的 Origin 列表"""
        raw = os.environ.get('CORS_ORIGINS', '')
        if raw:
            import re
            return [o.strip() for o in re.split(r'[,;\s]+', raw) if o.strip()]
        return [
            cls.APP_BASE_URL,
            'https://brain.obrive.com',
            'http://localhost:3000',
            'http://127.0.0.1:3000',
        ]

    @classmethod
    def validate(cls) -> list[str]:
        """验证必要配置"""
        errors: list[str] = []
        if not cls.LLM_API_KEY:
            errors.append("LLM_API_KEY 未配置")
        if not cls.get_zep_api_keys():
            errors.append("ZEP_API_KEY 未配置")
        if os.environ.get("ZEP_API_URL"):
            errors.append('ZEP_API_URL not supported; Brain only connects to Zep Cloud')
        if not cls.DEBUG and cls.SECRET_KEY == 'brain-secret-key':
            import warnings
            warnings.warn("Using default SECRET_KEY in production is insecure. Set SECRET_KEY in .env", RuntimeWarning)
        if cls.DEBUG:
            import warnings
            warnings.warn("Flask DEBUG mode is enabled. Do not use in production.", RuntimeWarning)
        return errors
