import click
from api.extensions import db
from api.models.users import Product
from flask.cli import with_appcontext

@click.command("seed_products")
@with_appcontext
def seed_products():
    """Seed the database with initial data."""
    product1 = Product(
        name="Product 1",
        variant_group_id="1",
        sku="SKU1",
        category_id=1
    )

    product2 = Product(
        name="Product 2",
        variant_group_id="2",
        sku="SKU2",
        category_id=2
    )

    db.session.add(product1)
    db.session.add(product2)
    db.session.commit()
    print("Products seeded successfully!")

# Register CLI command with Flask
def register_commands(app):
    app.cli.add_command(seed_products)