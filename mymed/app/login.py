import json
from urllib.request import urlopen, Request
from flask_login import LoginManager

from mymed.models.user import UserProfile, Patron, Provider, Scheduler, Manager
from mymed.setup.loggers import LOGGERS

lm = LoginManager()
log = LOGGERS.Login


@lm.user_loader
def load_user(profile_id):
    return UserProfile.get(profile_id)


def verify_user(payload):
    token = payload.get('token')
    sub = payload.get('sub')
    profile = UserProfile.get_or_create(sub)

    # get latest user info from payload
    aud = payload.get('aud', [])
    user_info = dict()
    for item in aud:
        if 'https' in item:
            req = Request(item)
            req.add_header('Authorization', f"Bearer {token}")
            content = urlopen(req).read()
            info = json.loads(content)
            user_info[item] = info
            log.debug(json.dumps(user_info, indent=4))
    # update user info from payload
    for info in user_info.values():
        for key, value in info.items():
            if hasattr(profile, key):
                if getattr(profile, key) != value:
                    setattr(profile, key, value)
    # save changes
    profile.save()
    log.debug(json.dumps(profile.dictionary, indent=4))
    return profile
