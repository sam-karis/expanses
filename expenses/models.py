from datetime import datetime

from app import db
from sqlalchemy.orm import backref


class BaseModel(object):
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, onupdate=datetime.utcnow)


class Department(BaseModel, db.Model):
    __tablename__ = "department"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)


class Project(BaseModel, db.Model):
    __tablename__ = "project"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)


class Member(BaseModel, db.Model):
    __tablename__ = "member"
    # Making a naive assumption that a combination of name and dept is unique
    __table_args__ = (db.UniqueConstraint("name", "department_id"),)

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    department_id = db.Column(
        db.BigInteger,
        db.ForeignKey("department.id"),
    )

    department = db.relationship(
        "Department", backref=backref("members", lazy="dynamic")
    )


class Expense(BaseModel, db.Model):
    __tablename__ = "expense"

    id = db.Column(db.BigInteger, primary_key=True)
    member_id = db.Column(
        db.BigInteger,
        db.ForeignKey("member.id"),
        nullable=False,
    )
    project_id = db.Column(
        db.BigInteger,
        db.ForeignKey("project.id"),
        nullable=False,
    )
    date = db.Column(
        db.DateTime,
        nullable=False,
    )
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    currency_symbol = db.Column(db.String(), nullable=False, default="€")

    member = db.relationship("Member", backref=backref("expenses", lazy="dynamic"))
    project = db.relationship("Project", backref=backref("expenses", lazy="dynamic"))
