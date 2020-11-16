import os
from mymed.app import create_app
from mymed.db import db
import pytest


testing_config_yaml = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static', 'config.yaml')


@pytest.fixture
def fresh_app():
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
def fresh_anonymous_client(fresh_app):
    """
    Purpose: creates a test client for the application
    Returns: freshly instantiated client object
    """
    client = fresh_app.test_client()
    yield client


@pytest.fixture
def fresh_login_client(fresh_anonymous_client, fresh_encoded_jwt):
    """
    Purpose: creates a test client with Authorization header already attached
    Returns: a newly logged in test client for new user testing
    """
    token = fresh_encoded_jwt[0]
    fresh_anonymous_client.environ_base['HTTP_AUTHORIZATION'] = f"Bearer {token}"
    yield fresh_anonymous_client


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


@pytest.fixture(scope='module')
def module_client(module_app):
    """
    Purpose: creates a test client for the application
    Returns: freshly instantiated client object
    """
    client = module_app.test_client()
    client.preserve_context = True
    yield client


@pytest.fixture(scope='module')
def patron_only_client(module_client, module_credentials):
    patron_only = module_credentials[0]
    token = patron_only['token']
    module_client.environ_base['HTTP_AUTHORIZATION'] = f"Bearer {token}"
    response = module_client.get('auth/finalize/')
    assert response.status_code == 200
    yield module_client, patron_only
