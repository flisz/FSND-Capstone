from flask_login import UserMixin
from .base import Model
from mymed.db import db


__all__ = ('User',)


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
    role = db.Column(db.String(64), nullable=True)
    permissions = db.Column(db.String(64), nullable=True)
    context = db.relationship('Context', backref='context', lazy=True)

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
            'role': self.role,
            'permissions': self.permissions,
            'contexts': self.all_contexts_serialized
        }

    @property
    def all_contexts(self):
        return []

    @property
    def all_contexts_serialized(self):
        return []
