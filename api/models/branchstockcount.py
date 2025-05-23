from datetime import datetime, UTC
from api.extensions import db

class BranchStockCount(db.Model):
    __tablename__ = 'branchstockcount'

    branch_id = db.Column(db.Integer, db.ForeignKey('branches.branch_id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('inventoryitems.item_id'), primary_key=True)
    in_stock = db.Column(db.Float, nullable=False)
    ordered_qty = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))
    deleted_at = db.Column(db.DateTime)

    __table_args__ = (db.UniqueConstraint('branch_id', 'item_id', name='unique_branch_item'),)

    branch = db.relationship('Branch', back_populates='branchstockcounts')
    item = db.relationship('InventoryItem', back_populates='branchstockcounts')

    def __init__(self, branch_id, item_id, in_stock, ordered_qty):
        self.branch_id = branch_id
        self.item_id = item_id
        self.in_stock = in_stock
        self.ordered_qty = ordered_qty
