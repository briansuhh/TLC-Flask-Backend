import click
from api.extensions import db
from api.models.suppliers import Supplier
from flask.cli import with_appcontext

@click.command("seed_suppliers")
@with_appcontext
def seed_suppliers():
    """Seed the database with initial suppliers data."""

    suppliers = [
        Supplier(
            name="Egg Supplier",
            email="eggsupplier@gmail.com",
            phone="9991114444",
            country_code="+63"
        ),
        Supplier(
            name="Oil Supplier",
            email="oilsupplier@gmail.com",
            phone="9991115555",
            country_code="+1"
        ),
        Supplier(
            name="Rice Supplier",
            email="ricesupplier@gmail.com",
            phone="9991116666",
            country_code="+44-1534"
        )
    ]

    db.session.bulk_save_objects(suppliers)
    db.session.commit()
    print("Suppliers seeded successfully!")

# Register CLI command with Flask
def register_commands(app):
    app.cli.add_command(seed_suppliers)
