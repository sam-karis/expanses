from datetime import datetime
from functools import wraps
from flask import request


def validate_datetime(date_text, date_format="%m/%d/%Y"):
    try:
        datetime.strptime(date_text, date_format)
    except ValueError:
        return {
            "message": f"Incorrect date format, should by {date_format}",
            "status": "Error",
        }, 400


def validate_fields(fields):
    allowed_terms = ("department", "amount", "memberName", "project", "date")
    invalid_terms = []
    for term in fields:
        if term not in allowed_terms:
            invalid_terms.append(term)

    if invalid_terms:
        return {
            "message": f"Invalid fields, {invalid_terms}",
            "allowedTerms": allowed_terms,
            "status": "Error",
        }, 400


def validate_request(params={}):
    """
    Validate request params before execution of endpoint logic
    params: dict like(optional)
    returns: error or endpoint response
    """

    def request_view(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            allowed_params = [
                "sort",
                "order",
                "fields",
                "id",
                "project",
                "amount",
                "amount[gte]",
                "amount[gt]",
                "amount[lte]",
                "amount[lt]",
                "date",
                "date[gte]",
                "date[gt]",
                "date[lte]",
                "date[lt]",
                "memberName",
                "department",
            ]
            params = request.args

            for param in params:
                if param not in allowed_params:
                    return {
                        "status": "error",
                        "message": f"{param} is not allowed",
                        "allowedParams": allowed_params,
                    }, 400
                if param == "date":
                    date_is_valid = validate_datetime(params["date"])
                    if date_is_valid is not None:
                        return date_is_valid

                if param == "sort":
                    sort_fields = params["sort"].split(",")
                    sort_is_valid = validate_fields(sort_fields)
                    if sort_is_valid is not None:
                        return sort_is_valid

                if param == "fields":
                    fields = params["fields"].split(",")
                    is_valid = validate_fields(fields)
                    if is_valid is not None:
                        return is_valid
            return func(*args, **kwargs)

        return wrapper

    return request_view


def validate_aggregates_request(params={}):
    """
    Validate request params before execution of endpoint logic
    params: dict like(optional)
    returns: error or endpoint response
    """

    def request_view(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            group_by_allowed_terms = (
                "department",
                "memberName",
                "project",
                "date",
            )
            params = request.args
            if "by" not in params:
                return {
                    "status": "error",
                    "message": "by is a required parameter",
                }, 400
            if params["by"] not in group_by_allowed_terms:
                return {
                    "status": "error",
                    "message": f"{params['by']} is not allowed",
                    "allowedParams": group_by_allowed_terms,
                }, 400

            return func(*args, **kwargs)

        return wrapper

    return request_view
