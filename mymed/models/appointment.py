from arrow import utcnow
from sqlalchemy_utils import ArrowType
from sqlalchemy.ext.declarative import declared_attr

from .base import Model
from mymed.db import db


__all__ = ('Appointment',)


class Appointment(Model):
    """
    .base.Model provides:
        id (primary key)
        created_at (creation date)
    """
    name = db.Column(db.String(), nullable=False)
    context = db.relationship('Context', backref='context', lazy=True)

    @declared_attr
    def start_time(self):
        return db.Column(ArrowType, default=utcnow, nullable=False, index=True)

    def __repr__(self):
        return f'<Appointment {self.id} with start_time: {self.context_id} value: {self.value} units: {self.units}>'

    @property
    def all_contexts(self):
        return Context.query.filter(Context.appointment_id == self.id) \
            .order_by(Context.created_at)

    @property
    def dictionary(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'name': self.name,
            'start_time': self.start_time.isoformat(),
            'confirmed': self.confirmed,
            'contexts': self.all_contexts_serialized,
            'measurements': self.all_measurements_serialized,
        }