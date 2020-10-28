from flask_login import UserMixin
from .base import Model
from mymed.db import db


__all__ = ('User', 'Patron', 'Provider', 'Scheduler', 'Manager')


class User(UserMixin, Model):
    """
    .base.Model provides:
        id (primary key)
        created_at (creation date)
    flask_login.UserMixin provides:

    """

    alternate_id = db.Column(db.Integer, nullable=False, unique=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    patron = db.relationship('Patron', uselist=False, back_populates="user")
    provider = db.relationship('Provider', uselist=False, back_populates="user")
    scheduler = db.relationship('Scheduler', uselist=False, back_populates="user")
    manager = db.relationship('Manager', uselist=False, back_populates="user")

    def __repr__(self):
        return f'<User {self.id}: email: {self.email} nickname: {self.nickname}>'

    @property
    def dictionary(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'alternate_id': self.alternate_id,
            'social_id': self.social_id,
            'email': self.email,
            'records': self.all_records_serialized
        }

    @property
    def all_records(self):
        return []

    @property
    def all_records_serialized(self):
        return []


class Patron(Model):
    """
    .base.Model provides:
        id (primary key)
        created_at (creation date)
    """
    records = db.relationship('Records', backref='patron', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates='patron')

    def __repr__(self):
        return f'<Patron {self.id}: user_id: {self.user}>'

    @property
    def dictionary(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'records': self.alternate_id,
            'user_id': self.social_id,
            'user': self.email,
        }


class Provider(Model):
    """
    .base.Model provides:
        id (primary key)
        created_at (creation date)
    """
    records = db.relationship('Records', backref='provider', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'))
    active = db.Column(db.Boolean, default=False)


class Scheduler(Model):
    """
    .base.Model provides:
        id (primary key)
        created_at (creation date)
    """
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    appointments = db.relationship('Appointments', backref='scheduler', lazy=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'))
    active = db.Column(db.Boolean, default=False)


class Manager(Model):
    """
    .base.Model provides:
        id (primary key)
        created_at (creation date)
    """
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    schedulers = db.relationship('Scheduler', backref='manager', lazy=True)
    providers = db.relationship('Scheduler', backref='manager', lazy=True)
    active = db.Column(db.Boolean, default=False)
