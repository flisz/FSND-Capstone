from .base import Model

from mymed.db import db

__all__ = ('Address',)


user_address_association_table = db.Table('user_address_association', Model.metadata,
                                          db.Column('address_id', db.Integer, db.ForeignKey('address.id')),
                                          db.Column('userprofile_id', db.Integer, db.ForeignKey('userprofile.id')),
                                          )

scheduler_address_association_table = db.Table('scheduler_address_association', Model.metadata,
                                               db.Column('address_id', db.Integer, db.ForeignKey('address.id')),
                                               db.Column('scheduler_id', db.Integer, db.ForeignKey('scheduler.id')),
                                               )

manager_address_association_table = db.Table('manager_address_association', Model.metadata,
                                             db.Column('address_id', db.Integer, db.ForeignKey('address.id')),
                                             db.Column('manager_id', db.Integer, db.ForeignKey('manager.id')),
                                             )


class Address(Model):
    """
    Base Model Provides:
        id (primary key)
        created_at (creation date)
    """
    nickname = db.Column(db.String(), nullable=False)
    line1 = db.Column(db.String(), nullable=False)
    line2 = db.Column(db.String(), nullable=True)
    city = db.Column(db.String(), nullable=False)
    state = db.Column(db.String(), nullable=False)
    zip_code = db.Column(db.String(), nullable=False)
    user_profiles = db.relationship("UserProfile", secondary=user_address_association_table, backref="addresses")
    schedulers = db.relationship("Scheduler", secondary=scheduler_address_association_table, backref="addresses")
    managers = db.relationship("Manager", secondary=manager_address_association_table, backref="addresses")
    appointments = db.relationship("Appointment", backref="address")

    def __repr__(self):
        return f'<Address {self.id}>'

    @property
    def dictionary(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'line1': self.line1,
            'line2': self.line2,
            'city' : self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'user_profiles': self.all_users
            #'appointments': self.all_appointments todo upcoming and past appointments
        }

    @property
    def all_users_serialized(self):
        data = list()
        for user in self.user_profiles:
            data.append(user.nickname)
        return data


