import os
import pytest

import mymed.setup


testing_config_yaml = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static', 'config.yaml')


@pytest.fixture(scope='function')
def setup():
    """
    Purpose: used for unit tests of env_config
    Returns: freshly instantiated env object for each test case
    """
    return mymed.setup.SetupConfig(config_yaml=testing_config_yaml)
