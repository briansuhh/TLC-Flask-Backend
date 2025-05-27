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
    InventoryItem(name="Beef", cost=1.0, unit="kg", stock_warning_level=10, supplier_id=1),
    InventoryItem(name="Rice", cost=1.0, unit="kg", stock_warning_level=20, supplier_id=1),
    InventoryItem(name="Bacon", cost=1.0, unit="kg", stock_warning_level=8, supplier_id=1),
    InventoryItem(name="Spam", cost=1.0, unit="kg", stock_warning_level=6, supplier_id=1),
    InventoryItem(name="Tocino", cost=1.0, unit="kg", stock_warning_level=7, supplier_id=1),
    InventoryItem(name="Spanish Sardines", cost=1.0, unit="kg", stock_warning_level=5, supplier_id=1),
    InventoryItem(name="Bangus", cost=1.0, unit="kg", stock_warning_level=4, supplier_id=1),
    InventoryItem(name="Hungarian Sausage", cost=1.0, unit="kg", stock_warning_level=3, supplier_id=1),
    InventoryItem(name="Corned Beef", cost=1.0, unit="kg", stock_warning_level=6, supplier_id=1),
    InventoryItem(name="Longganisa", cost=1.0, unit="kg", stock_warning_level=5, supplier_id=1),
    InventoryItem(name="Eggs", cost=1.0, unit="pcs", stock_warning_level=16, supplier_id=1),
    InventoryItem(name="Cheese", cost=1.0, unit="kg", stock_warning_level=5, supplier_id=1),
    InventoryItem(name="Chicken", cost=1.0, unit="kg", stock_warning_level=8, supplier_id=1),
    InventoryItem(name="Pancit Noodles", cost=1.0, unit="kg", stock_warning_level=6, supplier_id=1),
    InventoryItem(name="Pork", cost=1.0, unit="kg", stock_warning_level=7, supplier_id=1),
    InventoryItem(name="Fish", cost=1.0, unit="kg", stock_warning_level=5, supplier_id=1),
    InventoryItem(name="Vegetables", cost=1.0, unit="kg", stock_warning_level=12, supplier_id=1),
    InventoryItem(name="Sugar", cost=1.0, unit="kg", stock_warning_level=10, supplier_id=1),
    InventoryItem(name="Milk", cost=1.0, unit="L", stock_warning_level=8, supplier_id=1),
    InventoryItem(name="Banana", cost=1.0, unit="kg", stock_warning_level=6, supplier_id=1),
    InventoryItem(name="Coconut", cost=1.0, unit="kg", stock_warning_level=4, supplier_id=1),
    InventoryItem(name="Cream Cheese", cost=1.0, unit="kg", stock_warning_level=6, supplier_id=1),
    InventoryItem(name="Butter", cost=1.0, unit="kg", stock_warning_level=5, supplier_id=1),
    InventoryItem(name="Flour", cost=1.0, unit="kg", stock_warning_level=12, supplier_id=1),
    InventoryItem(name="Chocolate", cost=1.0, unit="kg", stock_warning_level=8, supplier_id=1),
    InventoryItem(name="Ube", cost=1.0, unit="kg", stock_warning_level=4, supplier_id=1),
    InventoryItem(name="Carrot", cost=1.0, unit="kg", stock_warning_level=4, supplier_id=1),
    InventoryItem(name="Blueberry", cost=1.0, unit="kg", stock_warning_level=3, supplier_id=1),
    InventoryItem(name="Mango", cost=1.0, unit="kg", stock_warning_level=3, supplier_id=1),
    InventoryItem(name="Strawberry", cost=1.0, unit="kg", stock_warning_level=3, supplier_id=1),
    InventoryItem(name="Lemon", cost=1.0, unit="kg", stock_warning_level=2, supplier_id=1),
    InventoryItem(name="Coffee Beans", cost=1.0, unit="kg", stock_warning_level=20, supplier_id=1),
    InventoryItem(name="Condensed Milk", cost=1.0, unit="L", stock_warning_level=6, supplier_id=1),
    InventoryItem(name="Matcha Powder", cost=1.0, unit="kg", stock_warning_level=2, supplier_id=1),
    InventoryItem(name="Hazelnut Syrup", cost=1.0, unit="L", stock_warning_level=2, supplier_id=1),
    InventoryItem(name="Vanilla Syrup", cost=1.0, unit="L", stock_warning_level=2, supplier_id=1),
    InventoryItem(name="Caramel Syrup", cost=1.0, unit="L", stock_warning_level=2, supplier_id=1),
    InventoryItem(name="Rice Meal Box", cost=1.0, unit="pcs", stock_warning_level=40, supplier_id=1),
    InventoryItem(name="Rice Wrapper", cost=1.0, unit="pcs", stock_warning_level=40, supplier_id=1),
    InventoryItem(name="Disposable Spoon", cost=1.0, unit="pcs", stock_warning_level=100, supplier_id=1),
    InventoryItem(name="Disposable Fork", cost=1.0, unit="pcs", stock_warning_level=100, supplier_id=1),
    InventoryItem(name="Plastic Cup", cost=1.0, unit="pcs", stock_warning_level=60, supplier_id=1),
    InventoryItem(name="Straw", cost=1.0, unit="pcs", stock_warning_level=80, supplier_id=1),
]

        
    # Bulk insert the inventory items into the database
    db.session.bulk_save_objects(inventory_items)
    db.session.commit()
    print("Inventory items seeded successfully!")

# Register the CLI command with Flask
def register_commands(app):
    app.cli.add_command(seed_inventory_items)
