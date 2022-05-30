from datetime import datetime

import pandas as pd
from app import db
from flask import Blueprint

from expenses.models import Department, Expense, Member, Project

bp = Blueprint("data", __name__)


class SeedDate:
    def __init__(self, file_path="expanses.csv") -> None:
        self.file_path = file_path
        self.df = self.read_csv_data()
        self.departments = self.get_unique_data("departments")
        self.projects = self.get_unique_data("project_name")

    def read_csv_data(self):
        df = pd.read_csv(
            self.file_path,
            parse_dates=[
                "date",
            ],
            date_parser=lambda x: datetime.strptime(x, "%m/%d/%Y"),
        )
        return df

    def get_unique_data(self, column_name):
        result = []
        for item in self.df[column_name].unique():
            result.append({"name": item})
        return result

    def intial_data_seed(self, model, column_name):
        data = self.get_unique_data(column_name)
        return self.data_seed(model, data)

    def data_seed(self, model, data):
        db_count = model.query.count()
        if db_count < 1:
            db.session.bulk_insert_mappings(model, data)
            db.session.commit()
            return f"{model.__tablename__.capitalize()} Data seeded successfully"
        return f"{model.__tablename__.capitalize()} data seeded already"

    def get_dept_project_ids(self, model):
        items = model.query.all()
        items_dict = {}
        for item in items:
            items_dict[item.name] = item.id
        return items_dict

    def initial_member_data_seed(self):
        depts = self.get_dept_project_ids(Department)
        members = (
            self.df.groupby(["departments", "member_name"])
            .size()
            .reset_index(name="Freq")
        )

        members_data = []

        for _, member in members.iterrows():
            members_data.append(
                {"name": member.member_name, "department_id": depts[member.departments]}
            )

        return self.data_seed(Member, members_data)

    def get_member_ids(self):
        members = Member.query.all()
        members_dict = {}
        for member in members:
            members_dict[f"{member.name}_{member.department.name}"] = member.id
        return members_dict

    def initial_expense_data_seed(self):
        members = self.get_member_ids()
        projects = self.get_dept_project_ids(Project)

        expenses_data = []

        for _, row in self.df.iterrows():
            expenses_data.append(
                {
                    "date": row.date,
                    "amount": float(row.amount.replace("€", "").replace(",", "")),
                    "member_id": members[f"{row.member_name}_{row.departments}"],
                    "project_id": projects[row.project_name],
                }
            )

        return self.data_seed(Expense, expenses_data)
