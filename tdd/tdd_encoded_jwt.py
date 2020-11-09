import pytest


def tdd_encoded_jwt_matches_payload(fresh_encoded_jwt, fresh_decoded_jwt):
    """
    GIVEN: a tuple including a fresh_encoded_jwt and its expected payload
    WHEN: the fresh_encoded_jwt payload is compared with the fresh_decoded_jwt
    THEN: the value will match
    """
    payload = fresh_encoded_jwt[1]
    assert payload == fresh_decoded_jwt
