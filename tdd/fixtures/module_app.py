import os
from mymed.app import create_app
from mymed.db import db
import pytest


testing_config_yaml = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static', 'config.yaml')


@pytest.fixture(scope='module')
def module_app():
    """
    Purpose: Sets up app/db for use by other fixtures
    Returns: freshly instantiated app object
    """
    app = create_app(config_yaml=testing_config_yaml)
    db.drop_all()
    db.create_all()
    yield app
    db.drop_all()


@pytest.fixture
def module_client(module_app):
    """
    Purpose: creates a test client for the application
    Returns: freshly instantiated client object
    """
    client = module_app.test_client()
    yield client


