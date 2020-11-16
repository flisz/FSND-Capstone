import jwt
import time
import pytest


fresh_jwt_payloads = [
    {
        "iss": "testing-payload",
        "sub": "mymed-test1|0001",
        "aud": ["mymed"],
        "iat": round(time.time()),
        "exp": round(time.time()) + 120,
        "azp": "testing-clientId",
        "scope": "openid"
    },
    {
        "iss": "testing-payload",
        "sub": "mymed-test1|0002",
        "aud": ["mymed"],
        "iat": round(time.time()),
        "exp": round(time.time()) + 120,
        "azp": "testing-clientId",
        "scope": "openid"
    }
]


@pytest.fixture(params=fresh_jwt_payloads)
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


module_jwt_payloads = [
    [
        {
            "case-name": "patron-only",
            "iss": "testing-payload",
            "sub": "mymed-test1|0001",
            "aud": ["mymed"],
            "iat": round(time.time()),
            "exp": round(time.time()) + 120,
            "azp": "testing-clientId",
            "scope": "openid"
        },
        {
            "case-name": "manager",
            "iss": "testing-payload",
            "sub": "mymed-test1|0002",
            "aud": ["mymed"],
            "iat": round(time.time()),
            "exp": round(time.time()) + 120,
            "azp": "testing-clientId",
            "scope": "openid"
        }
    ]
]


@pytest.fixture(params=module_jwt_payloads, scope='module')
def module_credentials(request, module_app):
    """
    Purpose: creates an encoded jwt for testing the context of a single logged in user
    Returns: a tuple including: the encoded_jwt, the secret, the algorithm and the payload
    """
    secret = module_app.config['SETUP'].JWT_SECRET
    algorithm = module_app.config['SETUP'].AUTH0_ALGORITHMS[0]
    payloads = request.param
    credentials = list()
    for payload in payloads:
        credential = dict()
        credential['case-name'] = payload.get('case-name')
        credential['payload'] = payload
        credential['token'] = jwt.encode(payload, secret, algorithm=algorithm).decode("utf-8")
        credentials.append(credential)
    return credentials





