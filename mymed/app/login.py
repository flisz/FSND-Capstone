from flask_login import LoginManager
from mymed.models.user import User


lm = LoginManager()


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
