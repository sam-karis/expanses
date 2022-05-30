from flask import Blueprint

bp = Blueprint("index", __name__)


@bp.route("/")
def index():
    return {"message": "This is index for expenses API"}, 200
