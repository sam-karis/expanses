"""
DAOS - Database Access (ORM)
Classes and methods for ineracting with the models and the database
"""
from datetime import datetime
from typing import List

from app import db

from expenses.models import Department, Expense, Member, Project


class BaseDao:
    def __init__(self, model: db.Model) -> None:
        self.model = model

    def get_all(self) -> List[db.Model]:
        return db.session.query(self.model).all()

    def get_by_id(self, value):
        return db.session.query(self.model).filter_by(id=value).first()

    def to_dict(self) -> dict:
        return {}


class MemberDao(BaseDao):
    def __init__(self, model: db.Model = Member) -> None:
        super().__init__(model)

    def get_by_name_department_id(self, name: str, id: int) -> Member:
        self.member = (
            db.session.query(self.model).filter_by(name=name, department_id=id).first()
        )
        return self.member

    def get_by_name_department(self, name: str, dept_name: int) -> Member:
        self.member = (
            db.session.query(Member.name, Department.name, Member.department_id)
            .filter(Member.department_id == Department.id)
            .filter(Member.name == name)
            .filter(Department.name == dept_name)
            .first()
        )
        return self.member

    def to_dict(self) -> dict:
        return {"name": self.member[0], "dept": self.member[1]}


class ExpenseDao(BaseDao):
    def __init__(self, model: db.Model = Expense) -> None:
        super().__init__(model)
        self.session = db.session
        self.return_fields = ("department", "amount", "memberName", "project", "date")

    @property
    def queryset(self) -> None:
        return (
            self.session.query(
                Member.name,
                Project.name,
                Department.name,
                Expense.date,
                Expense.amount,
                Expense.currency_symbol,
            )
            .filter(Expense.member_id == Member.id)
            .filter(Expense.project_id == Project.id)
            .filter(Member.department_id == Department.id)
        )

    def get_by_id(self, value):
        return self.queryset.filter_by(id=value).first()

    def single_member_expenses(self, member_name: str) -> None:
        self.expenses = self.queryset.filter(Member.name == member_name).all()

    def single_department_expenses(self, member_name: str, dept_name: str) -> None:
        self.expenses = self.queryset.filter(Department.name == dept_name).all()

    def single_member_department_expenses(
        self, member_name: str, dept_name: str
    ) -> None:
        self.expenses = (
            self.queryset.filter(Member.name == member_name)
            .filter(Department.name == dept_name)
            .all()
        )

    def date_to_string(self, date: datetime) -> str:
        return str(date.strftime("%m/%d/%Y"))

    def to_dict(self, expense=None, fields=None) -> dict:
        res = {}
        if expense is None:
            expense = self.expense
        if fields is None:
            fields = self.return_fields
        for field in fields:
            if field == "memberName":
                res["memberName"] = expense[0]
            if field == "project":
                res["project"] = expense[1]
            if field == "department":
                res["department"] = expense[2]
            if field == "date":
                res["date"] = self.date_to_string(expense[3])
            if field == "amount":
                res["amount"] = f"{expense[4]}{expense[5]}"
        return res

    def multiple_to_dict(self, expnses=None, fields=None):
        if expnses is None:
            expnses = self.expnses
        result = []
        for expense in expnses:
            result.append(self.to_dict(expense=expense, fields=fields))
        return result

    def aggregates_queryset(self, group_by) -> dict:
        queryset = (
            self.session.query(group_by, db.func.sum(Expense.amount).label("total"))
            .filter(Expense.member_id == Member.id)
            .filter(Expense.project_id == Project.id)
            .filter(Member.department_id == Department.id)
            .group_by(group_by)
        )
        return queryset

    def aggregates_to_dict(self, groups, by):
        result = []
        for group in groups:
            res = {"total": group[1]}
            if by == "date":
                res[by] = group[0].strftime("%m/%d/%Y")
            else:
                res[by] = group[0]
            result.append(res)
        return result


member_dao = MemberDao()
expense_dao = ExpenseDao()
