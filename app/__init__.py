from dotenv import load_dotenv
from flask import Flask

load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__)

    from .routes import main

    app.register_blueprint(main)
    app.config.from_object("config.Config")

    return app
