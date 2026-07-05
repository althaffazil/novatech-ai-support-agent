from flask import Flask

from src.core.application_container import ApplicationContainer
from src.web.routes import web_blueprint


def create_app() -> Flask:

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    container = ApplicationContainer()

    app.config["chat_service"] = container.chat_service

    app.register_blueprint(
        web_blueprint,
    )

    return app