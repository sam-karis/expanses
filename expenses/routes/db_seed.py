import click
from expenses.utils import SeedDate
from flask import Blueprint
from expenses.models import Department, Project

bp = Blueprint("data", __name__)


@bp.cli.command("seed")
@click.option("--m", "model_name", help="Optional Model Name", default="All")
def seed_data(model_name):
    click.echo(f"Starting the seeding data process for {model_name} model")
    data_instance = SeedDate()
    dept_response = data_instance.intial_data_seed(Department, "departments")
    click.echo(dept_response)
    project_response = data_instance.intial_data_seed(Project, "project_name")
    click.echo(project_response)
    member_response = data_instance.initial_member_data_seed()
    click.echo(member_response)
    expense_response = data_instance.initial_expense_data_seed()
    click.echo(expense_response)
