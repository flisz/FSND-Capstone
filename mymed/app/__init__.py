"""
Many thanks to Bob Waycott and Miguel Grinberg for excellent code examples and advice:
https://bobwaycott.com/blog/how-i-use-flask/organizing-flask-models-with-automatic-discovery/
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
"""

from copy import deepcopy
from flask import Flask

from mymed.setup import SetupConfig
from mymed.setup.loggers import LOGGERS
from mymed.app.csrf import csrf
from mymed.app.login import lm
from mymed.db import db, init_db
from mymed.views import init_views


log = LOGGERS.Setup


def create_app(config_yaml=None):
    """Default application factory.

    Default usage:
        app = create_app()

    Usage with config file:
        app = create_app('/path/to/config.yml')

    If config_file is not provided, will look for default
    config expected at '<proj_root>/config/config.yml'.
    Returns Flask app object.
    Raises EnvironmentError if config_file cannot be found.
    """

    setup = SetupConfig(config_yaml=config_yaml)

    # start app setup
    app = Flask(__name__, template_folder=setup.TEMPLATES, static_folder=setup.STATIC_FILES)
    app.config['SETUP'] = deepcopy(setup)
    app.config['SECRET_KEY'] = deepcopy(setup.SECRET_KEY)

    set_app_mode(app)
    lm.init_app(app)
    # setup csrf
    csrf.init_app(app)

    # setup db
    init_db(app, db)

    # register views
    init_views(app)



    return app


def set_app_mode(app):
    # set some helpful attrs to greatly simplify state checks
    cfg = app.config
    app.env = cfg.get('ENVIRONMENT', 'development')
    if app.debug:
        app.live = False
        if app.env == 'test':
            app.testing = True
        elif app.env == 'development':
            app.dev = True
        else:
            raise EnvironmentError('Invalid environment for app state.')
    else:
        if app.env == 'production':
            app.live = True
        elif app.env == 'development':
            # dev.proj runs in development with debug off
            app.live = False
            app.testing = False
        else:
            raise EnvironmentError('Invalid environment for app state.')
