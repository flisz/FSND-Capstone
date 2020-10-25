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
    created_by = db.Column(db.Integer, db.ForeignKey('creator.id'), nullable=False)
    patron_id = db.Column(db.Integer, db.ForeignKey('patron.id'), nullable=False)
    measurement_id = db.relationship('Measurement', backref='measurements', lazy=True)
    address_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=True)

    def __repr__(self):
        return f'<Context {self.id} measurement: {self.context_id} value: {self.value} units: {self.units}>'

    @property
    def measurements(self):
        return Measurement.query.filter(Measurement.context_id == self.id) \
            .order_by(Measurement.created_at)

    @property
    def measurements_serialized(self):
        return [measurement.dictionary for measurement in self.measurements]

    @property
    def number_of_measurements(self):
        return self.measurements.count()

    @property
    def dictionary(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'creator': self.creator.dictionary,
            'patron': self.patron.dicrionary,
            'provider': self.units,
            'measurement_count': self.number_of_measurements,
            'measurements': self.measurements_serialized,
            'appointment': self.value,
        }
