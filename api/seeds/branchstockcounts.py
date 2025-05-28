import click
from api.extensions import db
from api.models.branchstockcount import BranchStockCount
from flask.cli import with_appcontext
from datetime import datetime, UTC

@click.command("seed_branch_stock_counts")
@with_appcontext
def seed_branch_stock_counts():
    """Seed the database with initial branch stock count data."""
    
    # Define the initial data for branch stock counts
    branch_stock_counts = [
        BranchStockCount(
            branch_id=1,  # Assuming "TLC Mandaluyong" has ID 1
            item_id=1,    # Assuming "Item 1" has ID 1
            in_stock=100.0,
            ordered_qty=10.0
        ),
        BranchStockCount(
            branch_id=2,  # Assuming "TLC Manila" has ID 2
            item_id=2,    # Assuming "Item 2" has ID 2
            in_stock=50.0,
            ordered_qty=20.0
        ),
        BranchStockCount(
            branch_id=3,  # Assuming "TLC San Juan" has ID 3
            item_id=3,    # Assuming "Item 3" has ID 3
            in_stock=30.0,
            ordered_qty=5.0
        )
    ]
    
    # Bulk insert the branch stock counts into the database
    db.session.bulk_save_objects(branch_stock_counts)
    db.session.commit()
    print("Branch stock counts seeded successfully!")

# Register CLI command with Flask
def register_commands(app):
    app.cli.add_command(seed_branch_stock_counts)
