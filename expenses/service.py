from sqlalchemy import desc
from app import db
from expenses.models import Expense, Member, Department, Project
from expenses.daos import expense_dao


class ExpenseService:
    def __init__(self, params) -> None:
        self.params = params
        self.dao = expense_dao
        self.oparators = {
            "[gte]": ">=",
            "[gt": ">",
            "[lte]": "<=",
            "[lt]": "<",
            "": "==",
        }

    def get_expense_by_id(self) -> dict:
        id = self.params["id"]
        expense = self.dao.get_by_id(id)
        return self.dao.to_dict(expense)

    def expense_amount_filter(self, queryset):
        if self.params.get("amount[gte]") is not None:
            queryset = queryset.filter(Expense.amount >= self.params["amount[gte]"])
        if self.params.get("amount[gt]") is not None:
            queryset = queryset.filter(Expense.amount > self.params["amount[gt]"])
        if self.params.get("amount[lte]") is not None:
            queryset = queryset.filter(Expense.amount <= self.params["amount[lte]"])
        if self.params.get("amount[lt]") is not None:
            queryset = queryset.filter(Expense.amount < self.params["amount[lt]"])
        if self.params.get("amount") is not None:
            queryset = queryset.filter(Expense.amount == self.params["amount"])
        return queryset

    def expense_date_filter(self, queryset):
        if self.params.get("date[gte]") is not None:
            queryset = queryset.filter(Expense.date >= self.params["date[gte]"])
        if self.params.get("date[gt]") is not None:
            queryset = queryset.filter(Expense.date > self.params["date[gt]"])
        if self.params.get("date[lte]") is not None:
            queryset = queryset.filter(Expense.date <= self.params["date[lte]"])
        if self.params.get("date[lt]") is not None:
            queryset = queryset.filter(Expense.date < self.params["date[lt]"])
        if self.params.get("date") is not None:
            queryset = queryset.filter(Expense.date == self.params["date"])
        return queryset

    def expense_sort_order(self, queryset):
        sort_terms = self.params["sort"].split(",")
        is_desc = self.params.get("order") == "desc"
        for term in sort_terms:
            if term == "department":
                queryset = (
                    queryset.order_by(Department.name.desc())
                    if is_desc
                    else queryset.order_by(Department.name)
                )
            if term == "memberName":
                queryset = (
                    queryset.order_by(Member.name.desc())
                    if is_desc
                    else queryset.order_by(Member.name)
                )
            if term == "project":
                queryset = (
                    queryset.order_by(Project.name.desc())
                    if is_desc
                    else queryset.order_by(Project.name)
                )
            if term == "amount":
                queryset = (
                    queryset.order_by(Expense.amount.desc())
                    if is_desc
                    else queryset.order_by(Expense.amount)
                )
            if term == "date":
                queryset = (
                    queryset.order_by(Expense.date.desc())
                    if is_desc
                    else queryset.order_by(Expense.date)
                )
        return queryset

    def get_expenses_data(self) -> dict:
        queryset = self.dao.queryset
        if "memberName" in self.params:
            queryset = queryset.filter(Member.name == self.params["memberName"])
        if "department" in self.params:
            queryset = queryset.filter(Department.name == self.params["department"])
        if "project" in self.params:
            queryset = queryset.filter(Project.name == self.params["project"])
        if "amount" in str(self.params):
            queryset = self.expense_amount_filter(queryset)
        if "date" in str(self.params):
            queryset = self.expense_date_filter(queryset)
        if "sort" in self.params:
            queryset = self.expense_sort_order(queryset)
        expenses = queryset.all()
        fields = self.params.get("fields")
        if fields:
            fields = fields.split(",")
        return self.dao.multiple_to_dict(expenses, fields)

    def get_expenses_aggregates(self) -> dict:
        params_map = {
            "department": Department.name,
            "memberName": Member.name,
            "project": Project.name,
            "date": Expense.date,
        }
        queryset = self.dao.aggregates_queryset(params_map[self.params["by"]])
        result = queryset.all()
        return self.dao.aggregates_to_dict(result, self.params["by"])
