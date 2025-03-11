from datetime import datetime, UTC
from api.extensions import db

class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    variant_group_id = db.Column(db.String)
    sku = db.Column(db.String, nullable=False, unique=True)
    category_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))
    deleted_at = db.Column(db.DateTime)

    def __init__(self, name, variant_group_id, sku, category_id):
        self.name = name
        self.variant_group_id = variant_group_id
        self.sku = sku
        self.category_id = category_id

    def __repr__(self):
        return f'<Product {self.product_id}: {self.name}>'
