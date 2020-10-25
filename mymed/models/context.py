from .base import Model
from .measurement import Measurement
from mymed.db import db

__all__ = ('Context',)


class Context(Model):
    """
    Base Model Provides:
        id (primary key)
        created_at (creation date)
    """
    measurement_id = db.relationship('Measurement', backref='measurements', lazy=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=True)
    patron_id = db.Column(db.Integer, db.ForeignKey('patron.id'), nullable=False)

    def __repr__(self):
        return f'<Context {self.id} measurement: {self.context_id} value: {self.value} units: {self.units}>'

    @property
    def measurements(self):
        return Measurement.query.filter(Measurement.context_id == self.id) \
            .order_by(Measurement.created_at)

    @property
    def number_of_measurements(self):
        return self.measurements.count()

    @property
    def dictionary(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'measurements': self.description,
            'appointment': self.value,
            'provider': self.units,
            'valid': self.valid,
            'context_id': self.context_id,
            'patron_id': self.patron_id
        }
