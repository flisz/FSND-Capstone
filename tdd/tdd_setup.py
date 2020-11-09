import pytest
import os
import mymed.setup
import warnings


def tdd_SetupConfig_class_creation():
    """
    GIVEN: setup.setup_config import success
    WHEN: an SetupConfig object is instantiated
    THEN: an SetupConfig object is returned
    """
    setup = mymed.setup.SetupConfig()
    assert isinstance(setup, mymed.setup.SetupConfig)


def tdd_setup_fixture_is_SetupConfig(setup):
    """
    GIVEN: an setup tdd_fixture
    WHEN: setup fixture is passed to a test
    THEN: setup is an SetupConfig object
    """
    assert isinstance(setup, mymed.setup.SetupConfig)


def tdd_setup_CONFIG_is_dictionary(setup):
    """
    GIVEN: an setup tdd_fixture
    WHEN: setup fixture is passed to a test
    THEN: setup CONFIG property is a dictionary
    """
    assert isinstance(setup.CONFIG, dict)


def tdd_setup_MODE_is_valid(setup):
    """
    GIVEN: a setup tdd_fixture
    WHEN: MODE is requested
    THEN: MODE is 'test'
    """
    assert setup.APP_MODE == 'test'


def tdd_setup_APP_DOMAIN_is_valid(setup):
    """
    GIVEN: a setup fixture
    WHEN: setup.APP_DOMAIN is accessed
    THEN: a string with 'http' is returned
    """
    assert 'http' in setup.APP_DOMAIN


def tdd_setup_APP_HOST_is_valid(setup):
    """
    GIVEN: a setup fixture
    WHEN: setup.APP_HOST is accessed
    THEN: a string is returned
    """
    assert isinstance(setup.APP_HOST, str)


def tdd_setup_APP_PORT_is_valid(setup):
    """
    GIVEN: a setup fixture
    WHEN: setup.APP_PORT is accessed
    THEN: a string representation of an int is returned
    AND: the int is >4000 and <10000
    """
    assert isinstance(setup.APP_PORT, int)
    assert 4000 < setup.APP_PORT
    assert setup.APP_PORT < 10000


def tdd_setup_AUTH0_DOMAIN_is_str(setup):
    """
    GIVEN: a setup tdd_fixture
    WHEN: AUTH0_DOMAIN attribute is requested
    THEN: a string with 'auth0.com' is returned
    """
    assert isinstance(setup.AUTH0_DOMAIN, str)
    assert 'auth0.com' in setup.AUTH0_DOMAIN


def tdd_setup_AUTH0_ALGORITHMS_is_valid(setup):
    """
    GIVEN: a setup fixture
    WHEN: AUTH0_ALGORITHMS is requested
    THEN: a list of strings with 'RS256' is returned
    """
    assert isinstance(setup.AUTH0_ALGORITHMS, list)
    assert len(setup.AUTH0_ALGORITHMS) == 1
    assert setup.AUTH0_ALGORITHMS[0] == 'HS256'


def tdd_setup_AUTH0_API_AUDIENCE_is_str(setup):
    """
    GIVEN: a setup fixture
    WHEN: setup.AUTH0_API_AUDIENCE is requested
    THEN: a string is returned
    """
    assert isinstance(setup.AUTH0_API_AUDIENCE, str)


def tdd_setup_AUTH0_CLIENT_ID_is_str(setup):
    """
    GIVEN: a setup fixture
    WHEN: setup.AUTH0_CLIENT_ID is requested
    THEN: a string is returned
    """
    assert isinstance(setup.AUTH0_CLIENT_ID, str)


def tdd_setup_AUTH0_CALLBACK_URL_is_valid(setup):
    """
    GIVEN: a setup fixture
    WHEN: setup.AUTH0_CALLBACK_URL is requested
    THEN: a string containing auth/callback is returned
    """
    assert isinstance(setup.AUTH0_CALLBACK_URL, str)
    assert 'auth/callback/' in setup.AUTH0_CALLBACK_URL
    assert setup.APP_DOMAIN in setup.AUTH0_CALLBACK_URL
    assert str(setup.APP_PORT) in setup.AUTH0_CALLBACK_URL


def tdd_setup_USER_HOME_isdir(setup):
    """
    GIVEN: an setup tdd fixture
    WHEN: setup.USER_HOME is accessed
    THEN: a string pointing to a valid directory is returned
    """
    assert os.path.isdir(setup.USER_HOME)


def tdd_setup_TEMPLATES_isdir(setup):
    """
    GIVEN: an setup tdd fixture
    WHEN: setup.TEMPLATES is accessed
    THEN: a string pointing to a valid directory is returned
    """
    assert os.path.isdir(setup.TEMPLATES)


def tdd_setup_STATIC_FILES_isdir(setup):
    """
    GIVEN: an setup tdd fixture
    WHEN: setup.STATIC_FILES is accessed
    THEN: a string pointing to a valid directory is returned
    """
    assert os.path.isdir(setup.STATIC_FILES)


def tdd_setup_ROOT_is_valid(setup):
    """
    GIVEN: an setup tdd_fixture
    WHEN: requesting ROOT property
    AND: return value is a directory
    THEN: directory contains 'tdd' and 'migration' directories
    AMD: directory contains an 'setup.PROJECT_NAME' directory
    """
    assert os.path.isdir(setup.ROOT)
    directory_contents = os.listdir(setup.ROOT)
    assert any([item == 'tdd' for item in directory_contents])
    assert any([item == 'migrations' for item in directory_contents])
    assert any([item == setup.PROJECT_NAME for item in directory_contents])


def tdd_setup_JWT_SECRET_is_valid(setup):
    """
    GIVEN: an setup tdd_fixture
    WHEN: setup.JWT_SECRET is accessed
    THEN: a string is returned
    """
    assert isinstance(setup.JWT_SECRET, str)


def tdd_setup_HOSTNAME_is_str(setup):
    """
    GIVEN: an setup tdd_fixture
    WHEN: the type of setup.HOSTNAME is requested
    THEN: it will be a string
    """
    assert isinstance(setup.HOSTNAME, str)
