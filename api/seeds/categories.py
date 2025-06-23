import click
from api.extensions import db
from api.models.categories import Category
from flask.cli import with_appcontext

@click.command("seed_categories")
@with_appcontext
def seed_categories():
    """Seed the database with initial Category data."""

    categories = [
        Category(name="Main Meals"),
        Category(name="Desserts"),
        Category(name="Appetizers"),
        Category(name="Beverages"),
        Category(name="Salads")
    ]

    # Bulk save the Category objects to the database
    db.session.bulk_save_objects(categories)
    db.session.commit()
    print("Categories seeded successfully!")

# Register CLI command with Flask
def register_commands(app):
    app.cli.add_command(seed_categories)
