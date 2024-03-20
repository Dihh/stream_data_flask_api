import os
import logging
from flask import Flask, request
from flask_migrate import Migrate
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from jwt_config import config_jwt

from db import db
from src.controllers.game_controller import blp as GameController
from src.controllers.system_date_controller import blp as SystemDateController
from src.controllers.viewers_controller import blp as ViewersController
import src.models # pylint: disable=unused-import

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def set_api_config(app: Flask) -> None:
    app.config["PROPAGATE_EXCEPTIONS"] = False
    app.config["API_TITLE"] = "Flask todos API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

def set_db(app: Flask) -> None:
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///data.db")
    db.init_app(app)
    Migrate(app, db)

def set_api(app: Flask) -> Api:
    api = Api(app)
    api.spec.components.security_scheme("bearerAuth", {
        "type": "http", "scheme": "bearer", "bearerFormat": "JWT"
    })
    return api

def set_jwt(app: Flask) -> None:
    app.config["JWT_SECRET_KEY"] = os.getenv(
        "JWT_SECRET_KEY", "cc878440-91e0-4a07-b893-ef83b97a3256"
    )
    jwt = JWTManager(app)
    config_jwt(jwt)

def register_blueprint(api: Api) -> None:
    api.register_blueprint(GameController)
    api.register_blueprint(SystemDateController)
    api.register_blueprint(ViewersController)


def sef_after_request(app: Flask):
    @app.after_request
    def after_request(response):
        method = request.method
        path = request.path
        status_code = response.status_code
        raw_response = response.response
        logging.info("%s %s : %s - %s", method, path, status_code, raw_response )
        return response


def create_app() -> Flask:
    app = Flask(__name__)

    set_api_config(app)
    set_db(app)
    api = set_api(app)
    set_jwt(app)
    register_blueprint(api)

    return app
