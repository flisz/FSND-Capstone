__author__ = 'franksziebert@gmail.com'

"""
Many thanks to Bob Waycott and Miguel Grinberg for excellent code examples and advice:
https://bobwaycott.com/blog/how-i-use-flask/organizing-flask-models-with-automatic-discovery/
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_utils import force_auto_coercion


from mymed.setup.loggers import LOGGERS
from mymed.lib.loaders import load_models

__all__ = ('db', 'init_db')

log = LOGGERS.Setup
# our global DB object (imported by models & views & everything else)
db = SQLAlchemy()
# support importing a functioning session query
query = db.session.query
# our global migrate object
migrate = Migrate()


def init_db(app=None, db=None):
    """
    Initializes the global database object used by the app.

    Code base courtesy of:
    https://bobwaycott.com/blog/how-i-use-flask/organizing-flask-models-with-automatic-discovery/

    """
    if isinstance(app, Flask) and isinstance(db, SQLAlchemy):
        force_auto_coercion()
        load_models()
        database_uri = make_db_uri(app)
        app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.app = app
        db.init_app(app)
        migrate.init_app(app, db)
        log.info(f'Database Successfully configured.')
    else:
        raise ValueError('Cannot init DB without db and app objects.')


def make_db_uri(app):
    """
    Creates a uri for the database
    """
    setup = app.config.get('SETUP')
    db_info = setup.DATABASE_INFO.get('database')
    config = setup.CONFIG

    DEFAULT_DATABASE_NAME = f'db_{config.get("project_name")}'

    # Collect username:
    username = db_info.get('username')

    # Collect password:
    password = db_info.get('password')
    skip_passwords = ['none', 'None', 'default']
    if any([password == skip for skip in skip_passwords]):
        password = None

    # Collect host:
    host = db_info.get('host', 'localhost')
    if host == 'default':
        host = 'localhost'

    # Collect port
    port = db_info.get('port', '5432')
    if port == 'default':
        port = '5432'

    # Collect database_name
    database_name = db_info.get('database_name', DEFAULT_DATABASE_NAME)
    if database_name == 'default':
        database_name = DEFAULT_DATABASE_NAME

    if setup.APP_MODE == 'test':
        database_name = f'{database_name}_testing'

    if password:
        userpass = '{}:{}@'.format(username, password)
    elif username:
        userpass = '{}@'.format(username)
    else:
        userpass = ''

    log.info(f'Connecting to database: {database_name}')
    database_path =  f'postgresql://{userpass}{host}:{port}/{database_name}'
    log.debug(f'database_path: {database_path}')
    return database_path

