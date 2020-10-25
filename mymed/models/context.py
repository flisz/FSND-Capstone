from .base import Model
from .measurement import Measurement
from mymed.db import db

__all__ = ('Context',)


class Context(Model):
    """
    Base Model Provides:
        pk (primary key)
        created_at (creation date)
    """
    measurement_pk = db.relationship('Measurement', backref='measurements', lazy=True)
    appointment_pk = db.Column(db.Integer, db.ForeignKey('appointments.pk'), nullable=True)
    provider_pk = db.Column(db.Integer, db.ForeignKey('provider.pk'), nullable=True)
    patron_pk = db.Column(db.Integer, db.ForeignKey('patron.pk'), nullable=False)

    def __repr__(self):
        return f'<Context {self.pk} measurement: {self.context_pk} value: {self.value} units: {self.units}>'

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
            'pk': self.pk,
            'created_at': self.created_at,
            'measurements': self.description,
            'appointment': self.value,
            'provider': self.units,
            'valid': self.valid,
            'context_pk': self.context_pk,
            'patron_pk': self.patron_pk
        }
