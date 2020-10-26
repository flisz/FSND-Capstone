from .base import Model
from .measurement import Measurement
from mymed.db import db

__all__ = ('Record',)


class Record(Model):
    """
    Base Model Provides:
        id (primary key)
        created_at (creation date)
    """
    patron_id = db.Column(db.Integer, db.ForeignKey('patron.id'), nullable=False)
    measurements = db.relationship('Measurement', backref='measurements', lazy=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'))

    def __repr__(self):
        return f'<Record {self.id} ' \
               f'patron_id: {self.patron_id} ' \
               f'provider_id: {self.provider_id} ' \
               f'appointment_id: {self.appointment_id}>'

    @property
    def measurements(self):
        return Measurement.query.filter(Measurement.record_id == self.id) \
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
            'patron': self.patron.dicrionary,
            'provider': self.provider.dictionary,
            'measurement_count': self.number_of_measurements,
            'measurements': self.measurements_serialized,
            'appointment': self.appointment,
        }
