from datetime import datetime
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class RoleEnum(Enum):
    USER = "User"
    ADMIN = "Admin"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.Enum(RoleEnum), default=RoleEnum.USER, nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    update_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
