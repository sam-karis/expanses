from flask import Blueprint, request

from expenses.validators import validate_request, validate_aggregates_request
from expenses.service import ExpenseService

bp = Blueprint("expenses", __name__)


@bp.route("/expanses_data/<id>")
@validate_request()
def expanse_by_id(id):
    expense_instance = ExpenseService({"id": id})
    return {
        "message": "Suceess",
        "data": expense_instance.get_expense_by_id(),
    }, 200


@bp.route("/expanses_data")
@validate_request()
def expanses_data():
    params = request.args
    expense_instance = ExpenseService(params)

    return {
        "message": "Suceess",
        "data": expense_instance.get_expenses_data(),
    }, 200


@bp.route("/aggregates")
@validate_aggregates_request()
def expanses_aggregates():
    params = request.args
    expense_instance = ExpenseService(params)

    return {
        "message": "Suceess",
        "data": expense_instance.get_expenses_aggregates(),
    }, 200
