from datetime import datetime, UTC
from api.extensions import db

class InventoryItem(db.Model):
    __tablename__ = 'inventoryitems'

    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String, nullable=False)
    stock_warning_level = db.Column(db.Float, nullable=False)
    supplier_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))
    deleted_at = db.Column(db.DateTime)

    branches = db.relationship('BranchStockCount', back_populates='item', cascade='all, delete-orphan')

    def __init__(self, name, cost, unit, stock_warning_level, supplier_id):
        self.name = name
        self.cost = cost
        self.unit = unit
        self.stock_warning_level = stock_warning_level
        self.supplier_id = supplier_id

    def __repr__(self):
        return f'<InventoryItem {self.item_id}: {self.name}>'
