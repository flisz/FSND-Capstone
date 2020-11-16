import json
import pytest


def tdd_get_api_userprofile_logged_out(fresh_anonymous_client):
    """
    GIVEN: an initialized app fresh_anonymous_client, not logged in
    WHEN: the /api/userprofile route is requested
    THEN: the status code is a 308 redirect
    AND: the response.location is 'http://localhost/api/userprofile/'
    """
    response = fresh_anonymous_client.get('/api/userprofile')
    assert response.status_code == 308
    assert response.location == 'http://localhost/api/userprofile/'
    #assert response.location == 'http://mymed.dev/api/userprofile/'


def tdd_get_api_userprofile_health_logged_out_redirects_followed(fresh_anonymous_client):
    """
    GIVEN: an initialized app fresh_anonymous_client, not logged in
    WHEN: the /api/userprofile/health route is requested
    THEN: the response.status_code is 401 "Not Authorized"
    AND: the response.is_json is True
    AND: the response.json's code field is 'authorization_header_missing'
    AND: the response.json's description field is 'Authorization header is expected.'
    """
    response = fresh_anonymous_client.get('/api/userprofile/health', follow_redirects=True)
    assert response.status_code == 401
    assert response.is_json
    assert response.json.get('code') == 'authorization_header_missing'
    assert response.json.get('description') == 'Authorization header is expected.'


def tdd_get_api_userprofile_health_for_new_user(patron_only_client):
    """
    GIVEN: a new user client who has just logged in
    WHEN: the /api/userprofile route is requested
    THEN: the response.status_code is 200
    AND: the response.is_json is True
    AND: the response.data is Healthy
    """
    client = patron_only_client[0]
    response = client.get('/api/userprofile/health', follow_redirects=True)
    assert response.status_code == 200
    assert response.data == b'Healthy'


def tdd_get_api_userprofile_for_new_user(patron_only_client):
    """
    GIVEN: a new user client who has just logged in
    WHEN: the /api/userprofile route is requested
    THEN: the response.status_code is 200
    AND: the response.is_json is True
    AND: the response.json contains all the fields in UserProfile.dictionary
    """
    client = patron_only_client[0]
    response = client.get('/api/userprofile/', follow_redirects=True)
    assert response.status_code == 200
    assert response.is_json
    assert response.json.get("id") == 1
    assert isinstance(response.json.get("created_at"), str)
    assert isinstance(response.json.get("alternate_id"), str)
    assert response.json.get("social_id") is None
    assert response.json.get("email") is None
    assert response.json.get("email_verified") is False
    assert response.json.get("name") is None
    assert response.json.get("family_name") is None
    assert response.json.get("given_name") is None
    assert response.json.get("locale") == "en"
    assert isinstance(response.json.get("updated_at"), str)
    assert response.json.get("my_patron_id") == 1
    assert response.json.get("my_provider_id") == 1
    assert response.json.get("my_scheduler_id") == 1
    assert response.json.get("my_manager_id") == 1


def tdd_patch_api_userprofile(patron_only_client):
    """
    GIVEN: a new user client who has just logged in
    WHEN: the /api/userprofile/<user.id> route is patched with valid fields
    AND: the response.is_json is True
    AND: the response.json's updated time will have changed
    AND: the response.json will contain all the new data sent to the api.
    """
    client = patron_only_client[0]
    data = {
        "id": 1,
        "email": "mynewmail@email.com",
        "name": 'Tuni',
        "family_name": 'Patronus',
        "given_name": 'Petunia'
    }
    patch_response = client.patch(f'/api/userprofile/', data=json.dumps(data))
    assert patch_response.status_code == 200
    assert patch_response.is_json
    for key, value in data.items():
        assert patch_response.json.get(key) == value
