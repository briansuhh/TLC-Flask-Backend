import click
from api.extensions import db
from api.models.users import User
from flask.cli import with_appcontext
from datetime import datetime

@click.command("seed_users")
@with_appcontext
def seed_users():
    """Seed the database with initial data."""
    user = [
        User(
            username="testing",
            first_name="Trial",
            middle_name="N",
            last_name="User",
            birth_date=datetime.strptime("2003-06-22", "%Y-%m-%d"),
            sex="M",
            position="Cashier",
            email="trialcashier1@example.com",
            password_hash="hashedpassword"
        ),
        User(
            username="test",
            first_name="Test",
            middle_name="N",
            last_name="User",
            birth_date=datetime.strptime("2003-06-22", "%Y-%m-%d"),
            sex="M",
            position="Cashier",
            email="trialcashier1@example.com",
            password_hash="hashedpassword"
        )
    ]

    db.session.bulk_save_objects(user)
    db.session.commit()
    print("Database seeded successfully!")

# Register CLI command with Flask
def register_commands(app):
    app.cli.add_command(seed_users)
