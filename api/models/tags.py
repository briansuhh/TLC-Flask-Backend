from datetime import datetime, UTC
from api.extensions import db

class Tag(db.Model):
    __tablename__ = 'tags'

    tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))
    deleted_at = db.Column(db.DateTime)

    products = db.relationship('ProductTag', back_populates='tag', cascade='all, delete-orphan')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Tag {self.tag_id}: {self.name}>'
