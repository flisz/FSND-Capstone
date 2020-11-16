import pytest


def tdd_root_health(fresh_anonymous_client):
    """
    GIVEN: an initialized app fresh_anonymous_client
    WHEN: the /health/ route is requested
    THEN: the response.status_code is 200
    THEN: the return data is 'Healthy
    """
    response = fresh_anonymous_client.get('/health/')
    assert response.status_code == 200
    assert response.data == b'Healthy'


def tdd_root_index_anonymous_client(fresh_anonymous_client):
    """
    GIVEN: an initialized app fresh_anonymous_client
    WHEN: the /health/ route is requested
    THEN: the response.status_code is 200
    AND: the response.content_length is 3314
    AND: the response.mimetype is text/html
    AND: the response.data has the correct "MyMed' title, "Sign In" text, and the site's tagline
    """
    response = fresh_anonymous_client.get('/')
    assert response.status_code == 200
    assert response.mimetype == 'text/html'
    assert response.content_length == 2898
    assert b'<title>MyMed</title>' in response.data
    assert b'<a class="nav-link" href="/auth/login/">Sign In</a>' in response.data
    assert b'<p class="lead">Helping people become the patrons of their wellness journey</p>' in response.data