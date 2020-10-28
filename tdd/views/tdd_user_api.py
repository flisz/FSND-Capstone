import pytest


def tdd_api_get_user_profile(client):
    """
    GIVEN: an initialized app client
    WHEN: the /health/ route is requested
    THEN: the status code is 200
    THEN: the return data is 'Healthy'
    """
    response = client.get('/api/profile')
    assert response.status_code == 200
    assert response.data == b'Healthy'