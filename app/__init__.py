from dotenv import load_dotenv
from flask import Flask

load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__)

    from .routes import auth_bp, verify_ar_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(verify_ar_bp)
    app.config.from_object("config.Config")

    return app
