import click
from api.extensions import db
from api.models.inventoryitems import InventoryItem 
from flask.cli import with_appcontext

@click.command("seed_inventory_items")
@with_appcontext
def seed_inventory_items():
    """Seed the database with initial inventory items data."""
    
    # Define the initial data for inventory items
    inventory_items = [
        InventoryItem(
            name="Item 1",
            cost=100.00,
            unit="kg",
            stock_warning_level=10.0,
            supplier_id=1
        ),
        InventoryItem(
            name="Item 2",
            cost=150.00,
            unit="kg",
            stock_warning_level=5.0,
            supplier_id=2
        ),
        InventoryItem(
            name="Item 3",
            cost=200.00,
            unit="lbs",
            stock_warning_level=20.0,
            supplier_id=1
        )
    ]
    
    # Bulk insert the inventory items into the database
    db.session.bulk_save_objects(inventory_items)
    db.session.commit()
    print("Inventory items seeded successfully!")

# Register the CLI command with Flask
def register_commands(app):
    app.cli.add_command(seed_inventory_items)
