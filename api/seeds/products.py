import click
from api.extensions import db
from api.models.users import Product
from flask.cli import with_appcontext

@click.command("seed_products")
@with_appcontext
def seed_products():
    """Seed the database with initial data."""

    products = [
        Product(
            name="Product 1",
            description="Description 1",
            price=100.00
        ),
        Product(
            name="Product 2",
            description="Description 2",
            price=200.00
        )
    ]

    
    db.session.bulk_save_objects(products)
    db.session.commit()
    print("Products seeded successfully!")

# Register CLI command with Flask
def register_commands(app):
    app.cli.add_command(seed_products)