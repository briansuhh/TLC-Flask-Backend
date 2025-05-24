from datetime import datetime, UTC
from api.extensions import db

class Recipe(db.Model):
    __tablename__ = 'recipes'

    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('inventoryitems.item_id'), primary_key=True)
    quantity = db.Column(db.Float, nullable=False)
    isTakeout = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))
    deleted_at = db.Column(db.DateTime)

    __table_args__ = (db.UniqueConstraint('product_id', 'item_id', name='unique_recipe_item'),)

    product = db.relationship('Product', back_populates='recipes')
    item = db.relationship('InventoryItem', back_populates='recipes')

    def __init__(self, product_id, item_id, quantity, isTakeout):
        self.product_id = product_id
        self.item_id = item_id
        self.quantity = quantity
        self.isTakeout = isTakeout

