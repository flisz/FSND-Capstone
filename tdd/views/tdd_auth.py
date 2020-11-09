import pytest


def tdd_auth_health(fresh_client):
    """
    GIVEN: an initialized app fresh_client
    WHEN: the /health/ route is requested
    THEN: the status code is 200
    THEN: the return data is 'Healthy
    """
    response = fresh_client.get('auth/health/')
    assert response.status_code == 200
    assert response.data == b'Healthy'


def tdd_auth_anonymous_login(fresh_client):
    """
    GIVEN: an anonymous app fresh_client
    WHEN: the /auth/login/ route is requested
    THEN: the response is a 302 redirect
    AND: the response is a redirect to the auth0 login site
    """
    response = fresh_client.get('auth/login/')
    auth0_domain = fresh_client.application.config['SETUP'].AUTH0_DOMAIN
    api_audience = fresh_client.application.config['SETUP'].AUTH0_API_AUDIENCE
    client_id = fresh_client.application.config['SETUP'].AUTH0_CLIENT_ID
    callback_url = fresh_client.application.config['SETUP'].AUTH0_CALLBACK_URL
    expected_location = f'https://{auth0_domain}/authorize' \
                        f'?audience={api_audience}' \
                        f'&response_type=token' \
                        f'&client_id={client_id}' \
                        f'&redirect_uri={callback_url}'

    assert response.status_code == 302
    assert response.location == expected_location


@pytest.mark.skip(reason="jwt_tokens for testing still in development")
def tdd_auth_finalizer_fail_401(fresh_client):
    """
    GIVEN: an anonymous fresh_client
    WHEN: the finalizer route is accessed
    THEN: an "UNAUTHORIZED" response is returned
    """
    assert False


def tdd_auth_finalizer_fresh_token(fresh_client, fresh_encoded_jwt):
    """
    GIVEN: an anonymous fresh_client and a fresh_encoded_jwt
    WHEN: the auth/finalize route is requested
    AND: the 'Authorization' Header is provided.
    THEN: the response.status_code is 200
    AND: TODO!!!!!!!!!!!!!!!!
    """

    token = fresh_encoded_jwt[0]
    headers = {"Authorization": f"Bearer {token}"}
    response = fresh_client.get('auth/finalize/', headers=headers)
    assert response.status_code == 200
    assert False



