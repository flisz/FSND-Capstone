from .base import Model
from mymed.db import db

__all__ = ('Measurement',)


class Measurement(Model):
    """
    Base Model Provides:
        id (primary key)
        created_at (creation date)
    """
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    value = db.Column(db.String(), nullable=False)
    units = db.Column(db.String(), nullable=False)
    valid = db.Column(db.Boolean, nullable=False, default=True)
    record_id = db.Column(db.Integer, db.ForeignKey('record.id'), nullable=False)

    def __repr__(self):
        return f'<Measurement {self.id} with record_id: {self.record_id} value: {self.value} units: {self.units}>'

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
            'record_id': self.record.id,
        }
