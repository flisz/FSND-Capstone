import pytest


def tdd_get_api_userprofile_logged_out(client):
    """
    GIVEN: an initialized app client, not logged in
    WHEN: the /api/userprofile route is requested
    THEN: the status code is 303 "See Other"
    THEN: the target url is the login url
    """
    response = client.get('/api/userprofile')
    assert response.status_code == 303
    assert response.location == 'http://127.0.0.1/login'


