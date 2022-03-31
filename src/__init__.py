from flask import Flask
from .config.config import SECRET_KEY, JWT_SECRET_KEY, JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES, JWT_REFRESH_TOKEN_EXPIRES, JWT_TOKEN_LOCATION, JWT_QUERY_STRING_NAME
from .api.v1.routes.auth import auth
from .api.v1.routes.note import note
from flask_jwt_extended import JWTManager


def create_app():

    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        JWT_SECRET_KEY=JWT_SECRET_KEY,
        JWT_ACCESS_TOKEN_EXPIRES=JWT_ACCESS_TOKEN_EXPIRES,
        JWT_REFRESH_TOKEN_EXPIRES=JWT_REFRESH_TOKEN_EXPIRES,
        JWT_TOKEN_LOCATION=JWT_TOKEN_LOCATION,
        JWT_QUERY_STRING_NAME=JWT_QUERY_STRING_NAME
    )

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(note)

    return app
