import click
from api.extensions import db
from api.models.inventoryitems import InventoryItem 
from flask.cli import with_appcontext

@click.command("seed_inventory_items")
@with_appcontext
def seed_inventory_items():
    """Seed the database with initial inventory items data."""
    
    inventory_items = [
        InventoryItem(name="Beef", cost=100.0, unit="kg", stock_warning_level=10, supplier_id=1),
        InventoryItem(name="Rice", cost=50.0, unit="kg", stock_warning_level=20, supplier_id=2),
        InventoryItem(name="Bacon", cost=120.0, unit="kg", stock_warning_level=8, supplier_id=1),
        InventoryItem(name="Spam", cost=110.0, unit="kg", stock_warning_level=6, supplier_id=2),
        InventoryItem(name="Tocino", cost=130.0, unit="kg", stock_warning_level=7, supplier_id=1),
        InventoryItem(name="Spanish Sardines", cost=140.0, unit="kg", stock_warning_level=5, supplier_id=2),
        InventoryItem(name="Bangus", cost=150.0, unit="kg", stock_warning_level=4, supplier_id=1),
        InventoryItem(name="Hungarian Sausage", cost=160.0, unit="kg", stock_warning_level=3, supplier_id=2),
        InventoryItem(name="Corned Beef", cost=170.0, unit="kg", stock_warning_level=6, supplier_id=1),
        InventoryItem(name="Longganisa", cost=180.0, unit="kg", stock_warning_level=5, supplier_id=2),
        InventoryItem(name="Eggs", cost=90.0, unit="dozen", stock_warning_level=16, supplier_id=1),
        InventoryItem(name="Cheese", cost=200.0, unit="kg", stock_warning_level=5, supplier_id=2),
        InventoryItem(name="Chicken", cost=220.0, unit="kg", stock_warning_level=8, supplier_id=1),
        InventoryItem(name="Pancit Noodles", cost=70.0, unit="kg", stock_warning_level=6, supplier_id=2),
        InventoryItem(name="Pork", cost=240.0, unit="kg", stock_warning_level=7, supplier_id=1),
        InventoryItem(name="Fish", cost=130.0, unit="kg", stock_warning_level=5, supplier_id=2),
        InventoryItem(name="Vegetables", cost=60.0, unit="kg", stock_warning_level=12, supplier_id=1),
        InventoryItem(name="Sugar", cost=50.0, unit="kg", stock_warning_level=10, supplier_id=2),
        InventoryItem(name="Milk", cost=80.0, unit="liters", stock_warning_level=8, supplier_id=1),
        InventoryItem(name="Banana", cost=30.0, unit="kg", stock_warning_level=6, supplier_id=2),
        InventoryItem(name="Coconut", cost=20.0, unit="pcs", stock_warning_level=4, supplier_id=1),
        InventoryItem(name="Cream Cheese", cost=300.0, unit="kg", stock_warning_level=6, supplier_id=2),
        InventoryItem(name="Butter", cost=250.0, unit="kg", stock_warning_level=5, supplier_id=1),
        InventoryItem(name="Flour", cost=60.0, unit="kg", stock_warning_level=12, supplier_id=2),
        InventoryItem(name="Chocolate", cost=400.0, unit="kg", stock_warning_level=8, supplier_id=1),
        InventoryItem(name="Ube", cost=150.0, unit="kg", stock_warning_level=4, supplier_id=2),
        InventoryItem(name="Carrot", cost=100.0, unit="kg", stock_warning_level=4, supplier_id=1),
        InventoryItem(name="Blueberry", cost=500.0, unit="kg", stock_warning_level=3, supplier_id=2),
        InventoryItem(name="Mango", cost=300.0, unit="kg", stock_warning_level=3, supplier_id=1),
        InventoryItem(name="Strawberry", cost=350.0, unit="kg", stock_warning_level=3, supplier_id=2),
        InventoryItem(name="Lemon", cost=200.0, unit="kg", stock_warning_level=2, supplier_id=1),
        InventoryItem(name="Coffee Beans", cost=100.0, unit="kg", stock_warning_level=20, supplier_id=2),
        InventoryItem(name="Condensed Milk", cost=30.0, unit="kg", stock_warning_level=6, supplier_id=1),
        InventoryItem(name="Matcha Powder", cost=10.0, unit="kg", stock_warning_level=2, supplier_id=2),
        InventoryItem(name="Hazelnut Syrup", cost=10.0, unit="kg", stock_warning_level=2, supplier_id=1),
        InventoryItem(name="Vanilla Syrup", cost=10.0, unit="kg", stock_warning_level=2, supplier_id=2),
        InventoryItem(name="Caramel Syrup", cost=10.0, unit="kg", stock_warning_level=2, supplier_id=1),
        InventoryItem(name="Rice Meal Box", cost=5.0, unit="pcs", stock_warning_level=40, supplier_id=2),
        InventoryItem(name="Rice Wrapper", cost=5.0, unit="pcs", stock_warning_level=40, supplier_id=1),
        InventoryItem(name="Disposable Spoon", cost=0.05, unit="pcs", stock_warning_level=100, supplier_id=2),
        InventoryItem(name="Disposable Fork", cost=0.05, unit="pcs", stock_warning_level=100, supplier_id=1),
        InventoryItem(name="Plastic Cup", cost=0.1, unit="pcs", stock_warning_level=60, supplier_id=2),
        InventoryItem(name="Straw", cost=0.1, unit="pcs", stock_warning_level=80, supplier_id=1),
    ]
    
    db.session.bulk_save_objects(inventory_items)
    db.session.commit()
    print("Inventory items seeded successfully!")

# Register the CLI command with Flask
def register_commands(app):
    app.cli.add_command(seed_inventory_items)
