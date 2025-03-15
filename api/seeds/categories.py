import click
from api.extensions import db
from api.models.categories import Category
from flask.cli import with_appcontext

@click.command("seed_categories")
@with_appcontext
def seed_categories():
    """Seed the database with initial data."""
    category1 = Category(
        name="Main Meals"
    )

    category2 = Category(
        name="Desserts"
    )

    db.session.add(category1)
    db.session.add(category2)
    db.session.commit()
    print("Categories seeded successfully!")
    
# Register CLI command with Flask
def register_commands(app):
    app.cli.add_command(seed_categories)