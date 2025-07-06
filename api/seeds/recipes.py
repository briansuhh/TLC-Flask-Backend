import click
from api.extensions import db
from api.models.recipes import Recipe 
from flask.cli import with_appcontext

@click.command("seed_recipes")
@with_appcontext
def seed_recipes():
    """Seed the database with initial Recipe data."""
    
    recipes = [
        Recipe(product_id=1, item_id=1, quantity=1, isTakeout=False),
        Recipe(product_id=2, item_id=2, quantity=1, isTakeout=False),
        Recipe(product_id=3, item_id=4, quantity=1, isTakeout=False),
        Recipe(product_id=4, item_id=5, quantity=1, isTakeout=False),
        Recipe(product_id=5, item_id=6, quantity=1, isTakeout=False),
        Recipe(product_id=6, item_id=7, quantity=1, isTakeout=False),
        Recipe(product_id=7, item_id=8, quantity=1, isTakeout=False),
        Recipe(product_id=8, item_id=9, quantity=1, isTakeout=False),
        Recipe(product_id=9, item_id=10, quantity=1, isTakeout=False),
        Recipe(product_id=10, item_id=22, quantity=2, isTakeout=False),
        Recipe(product_id=11, item_id=23, quantity=2, isTakeout=False),
        Recipe(product_id=12, item_id=24, quantity=2, isTakeout=False),
        Recipe(product_id=13, item_id=25, quantity=2, isTakeout=False),
        Recipe(product_id=14, item_id=1, quantity=1, isTakeout=False),
        Recipe(product_id=15, item_id=26, quantity=1, isTakeout=False),
        Recipe(product_id=16, item_id=27, quantity=1, isTakeout=False),
        Recipe(product_id=17, item_id=28, quantity=1, isTakeout=False),
        Recipe(product_id=18, item_id=29, quantity=1, isTakeout=False),
        Recipe(product_id=19, item_id=22, quantity=2, isTakeout=False),
        Recipe(product_id=20, item_id=23, quantity=2, isTakeout=False),
        Recipe(product_id=21, item_id=24, quantity=2, isTakeout=False),
        Recipe(product_id=22, item_id=25, quantity=2, isTakeout=False),
        Recipe(product_id=23, item_id=26, quantity=2, isTakeout=False),
        Recipe(product_id=24, item_id=27, quantity=2, isTakeout=False),
        Recipe(product_id=25, item_id=28, quantity=2, isTakeout=False),
        Recipe(product_id=26, item_id=29, quantity=2, isTakeout=False),
        Recipe(product_id=27, item_id=30, quantity=2, isTakeout=False),
        Recipe(product_id=28, item_id=31, quantity=2, isTakeout=False),
        Recipe(product_id=29, item_id=32, quantity=2, isTakeout=False),
        Recipe(product_id=30, item_id=33, quantity=2, isTakeout=False),
        Recipe(product_id=31, item_id=34, quantity=2, isTakeout=False),
        Recipe(product_id=32, item_id=35, quantity=2, isTakeout=False),
        Recipe(product_id=33, item_id=36, quantity=1, isTakeout=False),
        Recipe(product_id=34, item_id=37, quantity=1, isTakeout=False),
        Recipe(product_id=35, item_id=38, quantity=1, isTakeout=False),
        Recipe(product_id=36, item_id=39, quantity=1, isTakeout=False),
        Recipe(product_id=37, item_id=40, quantity=1, isTakeout=False),
        Recipe(product_id=38, item_id=41, quantity=1, isTakeout=False),
        Recipe(product_id=39, item_id=42, quantity=1, isTakeout=False),
        Recipe(product_id=40, item_id=43, quantity=1, isTakeout=False),
        Recipe(product_id=44, item_id=38, quantity=1, isTakeout=False),
        Recipe(product_id=45, item_id=39, quantity=1, isTakeout=False),
    ]

    # Bulk save the Recipe objects to the database
    db.session.bulk_save_objects(recipes)
    db.session.commit()
    print("Recipes seeded successfully!")

# Register CLI command with Flask
def register_commands(app):
    app.cli.add_command(seed_recipes)
