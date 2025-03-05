from datetime import datetime, UTC
from api.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    first_name = db.Column(db.String, nullable=False)
    middle_name = db.Column(db.String)
    last_name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.Date)
    sex = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    password_age = db.Column(db.DateTime, default=datetime.now(UTC))
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))
    deleted_at = db.Column(db.DateTime)

    def __init__(self, username, first_name, middle_name, last_name, birth_date, sex, position, email, password_hash):
        self.username = username
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex
        self.position = position
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return f'<User {self.id}: {self.username}>'
