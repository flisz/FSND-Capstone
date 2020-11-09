import os
import jwt
import time
import base64
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
def fresh_client(fresh_app):
    """
    Purpose: creates a test client for the application
    Returns: freshly instantiated client object
    """
    client = fresh_app.test_client()
    yield client


jwt_payloads = [{
    "iss": "testing-payload",
    "sub": "mymed-test1|0001",
    "aud": ["mymed"],
    "iat": round(time.time()),
    "exp": round(time.time()) + 10,
    "azp": "testing-clientId",
    "scope": "openid"
}]


@pytest.fixture(params=jwt_payloads)
def fresh_encoded_jwt(request, fresh_app):
    """
    Purpose: creates an encoded jwt for single use minimal context testing
    Returns: a tuple including: the encoded_jwt, the secret, the algorithm and the payload
    """
    payload = request.param
    secret = fresh_app.config['SETUP'].JWT_SECRET
    algorithm = fresh_app.config['SETUP'].AUTH0_ALGORITHMS[0]
    encoded_jwt = jwt.encode(payload, secret, algorithm=algorithm).decode("utf-8")
    return encoded_jwt, payload, fresh_app


@pytest.fixture
def fresh_decoded_jwt(fresh_encoded_jwt):
    """
    Purpose: decodes a freshly encoded jwt
    Returns: a tuple including: the encoded_jwt, the payload, the jwt_secret
    """
    token = fresh_encoded_jwt[0]
    app = fresh_encoded_jwt[2]
    secret = app.config['SETUP'].JWT_SECRET
    algorithm = app.config['SETUP'].AUTH0_ALGORITHMS[0]
    audience = app.config['SETUP'].AUTH0_API_AUDIENCE
    payload = jwt.decode(token, secret, algorithms=algorithm, audience=audience, verify=True)
    return payload


