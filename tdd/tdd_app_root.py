import pytest


def tdd_root_health(client):
    response = client.get('/health/')
    assert response.status_code == 200
    assert response.data == b'Healthy'