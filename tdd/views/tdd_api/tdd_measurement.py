import pytest


def tdd_get_api_measurement_logged_out(fresh_anonymous_client):
    """
    GIVEN: an initialized app fresh_anonymous_client, not logged in
    WHEN: the /api/measurement route is requested
    THEN: the status code is a 308 redirect
    AND: the response.location is 'http://localhost/api/measurement/'
    THEN: the status code is 401 "Not Authorized"
    AND: the content is json
    AND: the content.json's code field is 'authorization_header_missing'
    AND: the con
    """
    response = fresh_anonymous_client.get('/api/measurement')
    assert response.status_code == 308
    assert response.location == 'http://localhost/api/measurement/'


def tdd_get_api_measurement_health_logged_out_redirects_followed(fresh_anonymous_client):
    """
    GIVEN: an initialized app fresh_anonymous_client, not logged in
    WHEN: the /api/measurement/health route is requested
    THEN: the response.status_code is 401 "Not Authorized"
    AND: the response.is_json is True
    AND: the response.json's code field is 'authorization_header_missing'
    AND: the response.json's description field is 'Authorization header is expected.'
    """
    response = fresh_anonymous_client.get('/api/measurement/health', follow_redirects=True)
    assert response.status_code == 401
    assert response.is_json
    assert response.json.get('code') == 'authorization_header_missing'
    assert response.json.get('description') == 'Authorization header is expected.'