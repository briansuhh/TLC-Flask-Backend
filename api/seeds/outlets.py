import click
from api.extensions import db
from api.models.outlets import Outlet
from flask.cli import with_appcontext

@click.command("seed_outlets")
@with_appcontext
def seed_outlets():
    """Seed the database with initial data."""
    outlets = [ 
        Outlet(product_id=1, name="In-Store", price=50.00),
        Outlet(product_id=1, name="GrabFood", price=52.00),
        Outlet(product_id=1, name="FoodPanda", price=53.00),
    ]

    db.session.bulk_save_objects(outlets)
    db.session.commit()
    print("Outlets seeded successfully!")

# Register CLI command with Flask
def register_commands(app):
    app.cli.add_command(seed_outlets)