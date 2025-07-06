import click
from api.extensions import db
from api.models.branchstockcount import BranchStockCount
from flask.cli import with_appcontext

@click.command("seed_branch_stock_counts")
@with_appcontext
def seed_branch_stock_counts():
    """Seed the database with initial branch stock count data."""
    
    branch_stock_counts = [
        # Branch 1 stock
        BranchStockCount(branch_id=1, item_id=1, in_stock=50, ordered_qty=10),
        BranchStockCount(branch_id=1, item_id=2, in_stock=100, ordered_qty=20),
        BranchStockCount(branch_id=1, item_id=3, in_stock=40, ordered_qty=8),
        BranchStockCount(branch_id=1, item_id=4, in_stock=30, ordered_qty=6),
        BranchStockCount(branch_id=1, item_id=5, in_stock=35, ordered_qty=7),
        BranchStockCount(branch_id=1, item_id=6, in_stock=25, ordered_qty=5),
        BranchStockCount(branch_id=1, item_id=7, in_stock=20, ordered_qty=4),
        BranchStockCount(branch_id=1, item_id=8, in_stock=15, ordered_qty=3),
        BranchStockCount(branch_id=1, item_id=9, in_stock=30, ordered_qty=6),
        BranchStockCount(branch_id=1, item_id=10, in_stock=25, ordered_qty=5),
        # Branch 2 stock
        BranchStockCount(branch_id=2, item_id=1, in_stock=60, ordered_qty=12),
        BranchStockCount(branch_id=2, item_id=2, in_stock=110, ordered_qty=22),
        BranchStockCount(branch_id=2, item_id=3, in_stock=45, ordered_qty=9),
        BranchStockCount(branch_id=2, item_id=4, in_stock=35, ordered_qty=7),
        BranchStockCount(branch_id=2, item_id=5, in_stock=40, ordered_qty=8),
        BranchStockCount(branch_id=2, item_id=6, in_stock=30, ordered_qty=6),
        BranchStockCount(branch_id=2, item_id=7, in_stock=25, ordered_qty=5),
        BranchStockCount(branch_id=2, item_id=8, in_stock=18, ordered_qty=3),
        BranchStockCount(branch_id=2, item_id=9, in_stock=35, ordered_qty=7),
        BranchStockCount(branch_id=2, item_id=10, in_stock=28, ordered_qty=6),
    ]
    
    db.session.bulk_save_objects(branch_stock_counts)
    db.session.commit()
    print("Branch stock counts seeded successfully!")

# Register CLI command with Flask
def register_commands(app):
    app.cli.add_command(seed_branch_stock_counts)
