import pytest


def tdd_get_api_userprofile_logged_out(fresh_client):
    """
    GIVEN: an initialized app fresh_client, not logged in
    WHEN: the /api/userprofile route is requested
    THEN: the status code is 401 "Not Authorized"
    AND:  the content is json
    AND:  the content's 'code' is
    """
    response = fresh_client.get('/api/userprofile')
    assert response.status_code == 308
    assert response.location == 'http://localhost/api/userprofile/'
    response = fresh_client.get('/api/userprofile', follow_redirects=True)
    assert response.status_code == 401
    assert response.is_json
    assert response.json.get('code') == 'authorization_header_missing'
    assert response.json.get('description') == 'Authorization header is expected.'


