import click
from api.extensions import db
from api.models.recipes import Recipe 
from flask.cli import with_appcontext

@click.command("seed_recipes")
@with_appcontext
def seed_recipes():
    """Seed the database with initial Recipe data."""
    
    recipes = [
        Recipe(
            product_id=1, 
            item_id=1,  
            quantity=10.5,
            isTakeout=True
        ),
        Recipe(
            product_id=2, 
            item_id=2,  
            quantity=20.0,
            isTakeout=False
        ),
        Recipe(
            product_id=3, 
            item_id=3, 
            quantity=15.0,
            isTakeout=True
        )
    ]

    # Bulk save the Recipe objects to the database
    db.session.bulk_save_objects(recipes)
    db.session.commit()
    print("Recipes seeded successfully!")

# Register CLI command with Flask
def register_commands(app):
    app.cli.add_command(seed_recipes)
