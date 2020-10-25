from .base import Model
from mymed.db import db

__all__ = ('Item',)


class Item(Model):
    """
    Base Model Provides:
        id (primary key)
        created_at (creation date)
    """
    summary = db.Column(db.String(), nullable=False)
    details = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)

    def __repr__(self):
        return f'<Item {self.id} details: {self.details} summary: {self.summary} active: {self.active} list_id: {self.list_id}>'

    @property
    def dictionary(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'summary': self.summary,
            'details': self.details,
            'active': self.active,
            'list_id': self.list_id
        }
