from flask_login import UserMixin
from .base import Model
from mymed.db import db


__all__ = ('User',)


class User(UserMixin, Model):
    """
    .base.Model provides:
        id (primary key)
        created_at (creation date)
    flask_login.UserMixin provides:

    """

    alternate_id = db.Column(db.Integer, nullable=False)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    address = db.relationship('Address', backref='address', lazy=True, nullable=True)
    role = db.Column(db.String(64), nullable=True)
    permissions = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        return f'<Measurement {self.id} with context: {self.context_id} value: {self.value} units: {self.units}>'

    @property
    def dictionary(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'name': self.name,
            'description': self.description,
            'value': self.value,
            'units': self.units,
            'valid': self.valid,
            'context_id': self.context_id,
            'patron_id': self.patron_id
        }