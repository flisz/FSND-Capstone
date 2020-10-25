from flask_login import UserMixin
from .base import Model
from mymed.db import db


__all__ = ('User',)


class User(UserMixin, Model):
    alternate_id = db.Column(db.Integer, nullable=False)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    address = db.relationship('Address', backref='address', lazy=True, nullable=True)
    role = db.Column(db.String(64), nullable=True)
    permissions = db.Column(db.String(64), nullable=True)

