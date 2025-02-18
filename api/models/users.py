from datetime import datetime, UTC
from api.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String)
    password_age = db.Column(db.DateTime, default=datetime.now(UTC))
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))
    deleted_at = db.Column(db.DateTime)

    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return f'<User {self.username}>'
