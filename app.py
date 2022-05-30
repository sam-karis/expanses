import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

from expenses.routes import db_seed, expenses  # noqa E402
from expenses.routes import index  # noqa E402
from expenses.routes import index  # noqa E402


def create_app(app_config=os.environ.get("APP_SETTINGS")):
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(app_config)
    app.url_map.strict_slashes = False

    db.init_app(app)
    migrate.init_app(app, db)

    from expenses import models  # noqa F401

    app.register_blueprint(index.bp, url_prefix="/")
    app.register_blueprint(expenses.bp, url_prefix="/")
    app.register_blueprint(db_seed.bp)

    return app
