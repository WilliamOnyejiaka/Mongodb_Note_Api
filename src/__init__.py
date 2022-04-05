from flask import Flask, render_template
from .config.config import SECRET_KEY, JWT_SECRET_KEY, JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES, JWT_REFRESH_TOKEN_EXPIRES, JWT_TOKEN_LOCATION, JWT_QUERY_STRING_NAME
from .api.v1.routes.auth import auth
from .api.v1.routes.note import note
from flask_jwt_extended import JWTManager
from flask_cors import CORS


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

    CORS(app, supports_credentials=True, resources={
        r"/*": {
            "origins": {
                "*",
            }
        }
    })

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(note)

    @app.errorhandler(404)
    def handle_404(e):
        return render_template("404.html")

    return app
