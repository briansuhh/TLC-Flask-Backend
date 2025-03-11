from datetime import datetime, UTC
from api.extensions import db

class Supplier(db.Model):
    __tablename__ = 'suppliers'

    supplier_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False, unique=True)
    country_code = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))
    deleted_at = db.Column(db.DateTime)

    def __init__(self, name, email, phone, country_code):
        self.name = name
        self.email = email
        self.phone = phone
        self.country_code = country_code

    def __repr__(self):
        return f'<Supplier {self.supplier_id}: {self.name}>'