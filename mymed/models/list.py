from .base import Model
from .item import Item
from mymed.db import db


__all__ = ('List',)


class List(Model):
    """
    Base Model Provides:
        id (primary key)
        created_at (creation date)
    """
    name = db.Column(db.String(), nullable=False)
    items = db.relationship('Item', backref='items', lazy=True)

    def __repr__(self):
        return f'<List {self.id} name: {self.name}>'

    @property
    def dictionary(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'name': self.name,
            'items': [item.dictionary for item in Item.query.filter(Item.list_id == self.id)]
        }
