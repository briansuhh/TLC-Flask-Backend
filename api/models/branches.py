from datetime import datetime, UTC
from api.extensions import db

class Branch(db.Model):
    __tablename__ = 'branches'

    branch_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    address = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))
    deleted_at = db.Column(db.DateTime)

    inventoryitems = db.relationship('BranchStockCount', back_populates='branch', cascade='all, delete-orphan')

    def __init__(self, name, address):
        self.name = name
        self.address = address

    def __repr__(self):
        return f'<Branch {self.branch_id}: {self.name}>'