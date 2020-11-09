import pytest


def tdd_root_health(fresh_client):
    """
    GIVEN: an initialized app fresh_client
    WHEN: the /health/ route is requested
    THEN: the status code is 200
    THEN: the return data is 'Healthy
    """
    response = fresh_client.get('/health/')
    assert response.status_code == 200
    assert response.data == b'Healthy'


def tdd_root_index_anonymous_cliet(fresh_client):
    """
    GIVEN: an initialized app fresh_client
    WHEN: the /health/ route is requested
    THEN: the status code is 200
    THEN: the return data is 'Healthy
    """
    response = fresh_client.get('/health/')
    assert response.status_code == 200
    assert response.data == b'Healthy'