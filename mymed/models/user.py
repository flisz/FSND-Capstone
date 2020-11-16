from flask_login import UserMixin
from .base import Model
from mymed.db import db
from sqlalchemy_utils import ArrowType
from arrow import utcnow

__all__ = ('UserProfile', 'Patron', 'Provider', 'Scheduler', 'Manager')


TIMEZONE = 'US/Mountain'


class UserProfile(UserMixin, Model):
    """
    .base.Model provides:
        id (primary key)
        created_at (creation date)
    flask_login.UserMixin provides:

    .address.Address.Model provides:
        addresses (collection)

    .record.Record.Model provides:
        records (collection)

    """

    alternate_id = db.Column(db.String(256), nullable=False, unique=True)
    social_id = db.Column(db.String(256), nullable=True, unique=True)
    nickname = db.Column(db.String(256), nullable=True)
    email = db.Column(db.String(256), nullable=True)
    picture = db.Column(db.String(256), nullable=True)
    name = db.Column(db.String(256), nullable=True)
    family_name = db.Column(db.String(256), nullable=True)
    given_name = db.Column(db.String(256), nullable=True)
    locale = db.Column(db.String(16), default='en', nullable=False)
    updated_at = db.Column(ArrowType, default=utcnow, index=True)
    email_verified = db.Column(db.Boolean, nullable=True, default=False)
    patron = db.relationship('Patron', uselist=False, back_populates="userprofile")  # 1-to-1
    provider = db.relationship('Provider', uselist=False, back_populates="userprofile")  # 1-to-1
    scheduler = db.relationship('Scheduler', uselist=False, back_populates="userprofile")  # 1-to-1
    manager = db.relationship('Manager', uselist=False, back_populates="userprofile")  # 1-to-1

    def __repr__(self):
        return f'<User {self.id}: email: {self.email} nickname: {self.nickname}>'

    @property
    def dictionary(self):
        return {
            'id': self.id,
            'created_at': str(self.created_at.to(TIMEZONE)),
            'alternate_id': self.alternate_id,
            'social_id': self.social_id,
            'email': self.email,
            'email_verified': self.email_verified,
            'name': self.name,
            'family_name': self.family_name,
            'given_name': self.given_name,
            'locale': self.locale,
            'updated_at': str(self.updated_at.to(TIMEZONE)),
            'my_patron_id': self.patron.id,
            'my_provider_id': self.provider.id,
            'my_scheduler_id': self.scheduler.id,
            'my_manager_id': self.manager.id
        }

    @property
    def all_records(self):
        return []

    @property
    def all_records_serialized(self):
        return []

    @classmethod
    def get_or_create(cls, sub):
        existing_user = cls.query.filter(cls.alternate_id == sub).one_or_none()
        if existing_user:
            return existing_user
        else:
            new_user = cls(alternate_id=sub)
            new_user.save()

            patron = Patron(userprofile=new_user, userprofile_id=new_user.id)
            patron.save()
            new_user.patron = patron
            new_user.save()

            provider = Provider(userprofile=new_user, userprofile_id=new_user.id)
            provider.save()
            new_user.provider = provider
            new_user.save()

            manager = Manager(userprofile=new_user, userprofile_id=new_user.id)
            manager.save()
            new_user.manager = manager
            new_user.save()

            scheduler = Scheduler(userprofile=new_user, userprofile_id=new_user.id)
            scheduler.save()
            new_user.scheduler = scheduler
            new_user.save()

            return new_user


class Patron(Model):
    """
    .base.Model provides:
        id (primary key)
        created_at (creation date)
    """
    records = db.relationship('Record', backref='patron', lazy=True)  # 1 to many
    userprofile_id = db.Column(db.Integer, db.ForeignKey('userprofile.id'))
    userprofile = db.relationship("UserProfile", back_populates='patron')

    def __repr__(self):
        return f'<Patron {self.id}: user_id: {self.user}>'

    @property
    def dictionary(self):
        return {
            'id': self.id,
            'created_at': str(self.created_at.to(TIMEZONE)),
            'records': self.id,
            'userprofile_id': self.userprofile_id,
            'userprofile': self.userprofile.dictionary,
        }


class Provider(Model):
    """
    .base.Model provides:
        id (primary key)
        created_at (creation date)
    .appointment.Appointment.Model provides
        appointments (through secondary table)
    """
    records = db.relationship('Record', backref='provider', lazy=True)
    userprofile_id = db.Column(db.Integer, db.ForeignKey('userprofile.id'))
    userprofile = db.relationship("UserProfile", back_populates='provider')
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'))
    active = db.Column(db.Boolean, default=False)


class Scheduler(Model):
    """
    .base.Model provides:
        id (primary key)
        created_at (creation date)
    .address.Address.Model provides:
        addresses (collection through secondary table)
    """
    userprofile_id = db.Column(db.Integer, db.ForeignKey('userprofile.id'))
    userprofile = db.relationship("UserProfile", back_populates='scheduler')
    appointments = db.relationship('Appointment', backref='scheduler', lazy=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'))
    active = db.Column(db.Boolean, default=False)


class Manager(Model):
    """
    .base.Model provides:
        id (primary key)
        created_at (creation date)
    .address.Address.Model provides:
        addresses (collection through secondary table)
    """
    userprofile_id = db.Column(db.Integer, db.ForeignKey('userprofile.id'))
    userprofile = db.relationship("UserProfile", back_populates='manager')
    schedulers = db.relationship('Scheduler', backref='manager', lazy=True)
    providers = db.relationship('Provider', backref='manager', lazy=True)
    active = db.Column(db.Boolean, default=False)
