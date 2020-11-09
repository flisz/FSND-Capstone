import pytest


@pytest.mark.skip(reason="no way of currently testing this")
def tdd_get_api_measurement_logged_out(fresh_client):
    """
    GIVEN: an initialized app fresh_client
    WHEN: the /health/ route is requested
    THEN: the status code is 200
    THEN: the return data is 'Healthy'
    """
    response = fresh_client.get('/api/profile')
    assert response.status_code == 200
    assert response.data == b'Healthy'