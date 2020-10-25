from flask_login import UserMixin
from .base import Model
from mymed.db import db


__all__ = ('User',)


class User(UserMixin, Model):
    alternate_id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)
