import os
from mymed.app import create_app
import pytest

testing_config_yaml = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static', 'config.yaml')

@pytest.fixture()
def app():
    """
    Purpose: Sets up app/db for use by other fixtures
    Returns: freshly instantiated app object
    """
    app = create_app(config_yaml=testing_config_yaml)
    return app


@pytest.fixture
def client(app):
    """
    Purpose: creates a test client for the application
    Returns: freshly instantiated client object
    """
    client = app.test_client()
    yield client


