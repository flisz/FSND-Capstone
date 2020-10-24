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
    GIVEN: and setup tdd_fixture
    WHEN: MODE is requested
    THEN: MODE is a valid value
    """
    valid_value_list = ['production', 'development', 'testing']
    assert any([setup.MODE == valid for valid in valid_value_list])
    warn_value_list = ['development']
    if any([setup.MODE == warn for warn in warn_value_list]):
        warnings.warn(UserWarning("mode is {} which should not be in production".format(setup.MODE)))


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


def tdd_setup_HOSTNAME_is_str(setup):
    """
    GIVEN: an setup tdd_fixture
    WHEN: the type of setup.HOSTNAME is requested
    THEN: it will be a string
    """
    assert isinstance(setup.HOSTNAME, str)
