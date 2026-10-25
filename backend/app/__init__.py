"""
Brain Backend - Flask Application Factory
"""

import os
import warnings

# 抑制 multiprocessing resource_tracker 的警告（来自第三方库如 transformers）
# 需要在所有其他导入之前设置
warnings.filterwarnings("ignore", message=".*resource_tracker.*")

from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
from flask_cors import CORS

from .config import Config
from .utils.logger import setup_logger, get_logger
from .models.user import db  # SQLAlchemy instance


def create_app(config_class=Config):
    """Flask应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 设置JSON编码：确保中文直接显示（而不是 \uXXXX 格式）
    # Flask >= 2.3 使用 app.json.ensure_ascii，旧版本使用 JSON_AS_ASCII 配置
    if hasattr(app, 'json') and hasattr(app.json, 'ensure_ascii'):
        app.json.ensure_ascii = False

    # Ensure SQLite parent directory exists if using SQLite
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if "sqlite" in db_uri:
        db_path = db_uri.replace("sqlite:///", "")
        if db_path and not db_path.startswith(":memory:"):
            try:
                os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
            except Exception:
                fallback_db = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../instance/brain_users.db"))
                os.makedirs(os.path.dirname(fallback_db), exist_ok=True)
                app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{fallback_db}"

    # Initialise SQLAlchemy (uses SQLALCHEMY_DATABASE_URI from Config)
    db.init_app(app)
    with app.app_context():
        # Enable WAL mode and busy timeout on SQLite to prevent 'database is locked' errors
        if "sqlite" in str(db.engine.url):
            try:
                from sqlalchemy import event
                @event.listens_for(db.engine, "connect")
                def _set_sqlite_pragma(dbapi_connection, connection_record):
                    cursor = dbapi_connection.cursor()
                    cursor.execute("PRAGMA journal_mode=WAL")
                    cursor.execute("PRAGMA synchronous=NORMAL")
                    cursor.execute("PRAGMA busy_timeout=5000")
                    cursor.close()
            except Exception:
                pass

        db.create_all()  # Create tables if they don't exist yet
        try:
            from sqlalchemy import inspect, text
            inspector = inspect(db.engine)
            if "users" in inspector.get_table_names():
                cols = [c["name"] for c in inspector.get_columns("users")]
                if "token_version" not in cols:
                    db.session.execute(text("ALTER TABLE users ADD COLUMN token_version INTEGER DEFAULT 1"))
                    db.session.commit()
                if "role" not in cols:
                    db.session.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user'"))
                    db.session.commit()
        except Exception:
            pass

        # Promote configured operator accounts to unlimited admin access.
        try:
            from .models.user import User
            admin_emails = Config.admin_emails()
            if admin_emails:
                users = User.query.filter(User.email.in_(admin_emails)).all()
                changed = False
                for user in users:
                    if user.role != "admin":
                        user.role = "admin"
                        changed = True
                if changed:
                    db.session.commit()
        except Exception:
            db.session.rollback()


    # 设置日志
    logger = setup_logger('brain')
    
    # 只在 reloader 子进程中打印启动信息（避免 debug 模式下打印两次）
    is_reloader_process = os.environ.get('WERKZEUG_RUN_MAIN') == 'true'
    debug_mode = app.config.get('DEBUG', False)
    should_log_startup = not debug_mode or is_reloader_process
    
    if should_log_startup:
        logger.info("=" * 50)
        logger.info('Brain Backend starting...')
        logger.info("=" * 50)
    
    # 启用CORS（使用配置的白名单域名，支持携带凭据）
    cors_origins = Config.get_cors_origins()
    CORS(app, resources={r"/api/*": {"origins": cors_origins}}, supports_credentials=True)
    
    # 注册模拟进程清理函数（确保服务器关闭时终止所有模拟进程）
    from .services.simulation_runner import SimulationRunner
    SimulationRunner.register_cleanup()
    if should_log_startup:
        logger.info("已注册模拟进程清理函数")
    
    # 请求日志中间件
    @app.before_request
    def log_request():
        logger = get_logger('brain.request')
        logger.debug(f"请求: {request.method} {request.path}")
        if request.content_type and 'json' in request.content_type:
            logger.debug(f"请求体: {request.get_json(silent=True)}")
    
    @app.after_request
    def set_security_headers_and_log(response):
        # 生产环境标准安全响应头
        response.headers.setdefault('X-Content-Type-Options', 'nosniff')
        response.headers.setdefault('X-Frame-Options', 'SAMEORIGIN')
        response.headers.setdefault('X-XSS-Protection', '1; mode=block')
        response.headers.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')

        logger = get_logger('brain.request')
        logger.debug(f"响应: {response.status_code}")
        return response

    # 全局 JSON 错误处理（确保 /api/* 始终返回结构化 JSON 而非 HTML 错误页）
    @app.errorhandler(400)
    def bad_request(e):
        if request.path.startswith('/api/'):
            return jsonify({
                "success": False,
                "error": getattr(e, "description", "Bad Request"),
                "code": "BAD_REQUEST"
            }), 400
        return e

    @app.errorhandler(404)
    def not_found(e):
        if request.path.startswith('/api/'):
            return jsonify({
                "success": False,
                "error": "Endpoint or resource not found",
                "code": "NOT_FOUND"
            }), 404
        return e

    @app.errorhandler(405)
    def method_not_allowed(e):
        if request.path.startswith('/api/'):
            return jsonify({
                "success": False,
                "error": "Method Not Allowed",
                "code": "METHOD_NOT_ALLOWED"
            }), 405
        return e

    @app.errorhandler(500)
    def internal_error(e):
        logger = get_logger('brain.app')
        logger.error(f"Internal error on {request.path}: {e}", exc_info=True)
        if request.path.startswith('/api/'):
            return jsonify({
                "success": False,
                "error": "Internal Server Error",
                "code": "INTERNAL_SERVER_ERROR"
            }), 500
        return e

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            if request.path.startswith('/api/'):
                return jsonify({
                    "success": False,
                    "error": e.description,
                    "code": f"HTTP_{e.code}"
                }), e.code
            return e

        logger = get_logger('brain.app')
        logger.error(f"Unhandled exception on {request.path}: {e}", exc_info=True)
        if request.path.startswith('/api/'):
            desc = str(e) if app.config.get('DEBUG') else "An unexpected error occurred."
            return jsonify({
                "success": False,
                "error": desc,
                "code": "UNEXPECTED_ERROR"
            }), 500
        raise e
    
    # 注册蓝图
    from .api import graph_bp, simulation_bp, report_bp
    from .api.auth import auth_bp
    from .api.billing import billing_bp
    app.register_blueprint(graph_bp, url_prefix='/api/graph')
    app.register_blueprint(simulation_bp, url_prefix='/api/simulation')
    app.register_blueprint(report_bp, url_prefix='/api/report')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(billing_bp, url_prefix='/api/billing')
    
    # 健康检查
    @app.route('/health')
    @app.route('/api/health')
    def health():
        return {'status': 'ok', 'service': 'Brain Backend'}
    
    if should_log_startup:
        logger.info('Brain Backend started')
    
    return app

