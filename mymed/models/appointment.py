from arrow import utcnow
from sqlalchemy_utils import ArrowType
from sqlalchemy.ext.declarative import declared_attr

from .base import Model
from .record import Record
from mymed.db import db


__all__ = ('Appointment',)


class Appointment(Model):
    """
    .base.Model provides:
        id (primary key)
        created_at (creation date)
    """
    name = db.Column(db.String(256), nullable=False)
    records = db.relationship('Record', backref='appointment', lazy=True)
    confirmed = db.Column(db.Boolean, default=False, nullable=False)
    held = db.Column(db.Boolean, default=False, nullable=False)
    cancelled = db.Column(db.Boolean, default=False, nullable=False)
    scheduler_id = db.Column(db.Integer, db.ForeignKey('scheduler.id'), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))

    @declared_attr
    def start_time(self):
        return db.Column(ArrowType, default=utcnow, nullable=False, index=True)

    def __repr__(self):
        return f'<Appointment {self.id} with start_time: {self.start_time.isoformat()}>'

    @property
    def all_records(self):
        return Record.query.filter(Record.appointment_id == self.id) \
            .order_by(Record.created_at)

    @property
    def all_records_serialized(self):
        return [record.dictionary for record in self.all_records]

    @property
    def dictionary(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'name': self.name,
            'address': self.address.dictionary,
            'start_time': self.start_time.isoformat(),
            'confirmed': self.confirmed,
            'cancelled': self.cancelled,
            'held': self.held,
            'records': self.all_records_serialized,
        }