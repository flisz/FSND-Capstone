from .base import Model
from mymed.db import db

__all__ = ('Measurement',)


class Measurement(Model):
    """
    Base Model Provides:
        pk (primary key)
        created_at (creation date)
    """
    description = db.Column(db.String(), nullable=True)
    value = db.Column(db.String(), nullable=False)
    units = db.Column(db.String(), nullable=False)
    valid = db.Column(db.Boolean, nullable=False, default=True)
    context_pk = db.Column(db.Integer, db.ForeignKey('context.pk'), nullable=False)
    patron_pk = db.Column(db.Integer, db.ForeignKey('user.pk'), nullable=False)


    def __repr__(self):
        return f'<Measurement {self.pk} with context: {self.context_pk} value: {self.value} units: {self.units}>'

    @property
    def dictionary(self):
        return {
            'pk': self.pk,
            'created_at': self.created_at,
            'description': self.description,
            'value': self.value,
            'units': self.units,
            'valid': self.valid, 
            'context_pk': self.context_pk,
            'patron_pk': self.patron_pk
        }
