import json
from flask import request, _request_ctx_stack, make_response, jsonify, abort, current_app
from flask_login import current_user, login_user
from functools import wraps
from jose import jwt
from urllib.request import urlopen

from mymed.setup.loggers import LOGGERS
from mymed.app.login import verify_user

log = LOGGERS.Auth


class AuthError(Exception):
    """
    AuthError Exception
        A standardized way to communicate auth failure modes
    """
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_cookie_session_token():
    try:
        return request.cookies.get('session')
    except Exception as e:
        log.exception(e)


def get_token_auth_header():
    """
    Obtains the Access Token from the Authorization Header
    :return token: jwt part of the header

    ** NOTE **
    Largely copied from practice exercises in course lessons.
    """

    # it should attempt to get the header from the request
    auth = request.headers.get('Authorization', None)
    log.debug(f'get_token_auth_header, got: {auth}')
    #   -> raise an AuthError if no header is present
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    # it should attempt to split bearer and the token
    parts = auth.split()
    #  -> raise an AuthError if the header is malformed
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    # return the token part of the header
    return token


def check_permissions(permission, payload):
    """
    Check the input permissions against the input payload to verify access.
    :param permission: string permission (i.e. 'post:drink')
    :param payload: decoded jwt payload
    :return True=>bool or raise an exception

    ** NOTE **
    Largely copied from practice exercises in course lessons.
    """
    # print(f'checking permission: {permission}')
    # print(json.dumps(payload, indent=4))
    # it should raise an AuthError if permissions are not included
    #    in the payload
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    # it should raise an AuthError if the requested permission string
    #    is not in the payload permissions array
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 401)
    return True


def verify_decode_jwt(token):
    """
    Verifies that the token in the Authorization header is valid.
    :param token: a json web token (string)
    :return: payload: decoded token dictionary

    !!NOTE urlopen has a common certificate error described here:
    https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org

    ** NOTE **
    Largely copied from practice exercises in course lessons.
    """

    # it should verify the token using Auth0 /.well-known/jwks.json
    log.debug(f'token: {token}')
    if not current_app.testing:
        jsonurl = urlopen(f'https://{current_app.config["SETUP"].AUTH0_DOMAIN}/.well-known/jwks.json')
        jwks = json.loads(jsonurl.read())
        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt.JWTError as e:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization malformed, Error decoding token headers.'
            }, 401)
        rsa_key = ''
        # it should be an Auth0 token with key id (kid)
        log.debug(json.dumps(unverified_header, indent=4))
        if 'kid' not in unverified_header:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization malformed.'
            }, 401)

        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }

        if rsa_key:
            # it should decode the payload from the token
            # it should validate the claims (which a lack of exceptions indicates)
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=current_app.config["SETUP"].AUTH0_ALGORITHMS,
                    audience=current_app.config["SETUP"].AUTH0_API_AUDIENCE,
                    issuer='https://' + current_app.config["SETUP"].AUTH0_DOMAIN + '/'
                )
                # return the decoded payload
                log.debug(json.dumps(payload, indent=4))
                return payload
            except jwt.ExpiredSignatureError:
                raise AuthError({
                    'code': 'token_expired',
                    'description': 'Token expired.'
                }, 401)
            except jwt.JWTClaimsError:
                raise AuthError({
                    'code': 'invalid_claims',
                    'description': 'Incorrect claims. Please, check the audience and issuer.'
                }, 401)
            except Exception:
                raise AuthError({
                    'code': 'invalid_header',
                    'description': 'Unable to parse authentication token.'
                }, 400)
        raise AuthError({
                    'code': 'invalid_header',
                    'description': 'Unable to find the appropriate key.'
                }, 400)
    else:
        secret = current_app.config['SETUP'].JWT_SECRET
        algorithm = current_app.config['SETUP'].AUTH0_ALGORITHMS[0]
        audience = current_app.config['SETUP'].AUTH0_API_AUDIENCE
        payload = jwt.decode(token, secret, algorithms=algorithm, audience=audience)
        log.debug(json.dumps(payload, indent=4))
        return payload


def view_requires_sign_in(f):
    """
    Decorator to require Authorization for a given route without any specific permissions
    :param f: function to wrap
    :return: function with wrapper
    """
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        try:
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            payload['token'] = token
            user = verify_user(payload)
            if current_user.is_anonymous:
                log.debug(f'signing in user: {user.alternate_id}')
                login_user(user)
            elif current_user.alternate_id != user.alternate_id:
                raise AuthError({
                    'code': 'client_session_already_bound',
                    'description': 'Session already bound to different user credentials.'
                }, 401)
        except AuthError as e:
            abort(make_response(jsonify(e.error), e.status_code))
        # self is a FlaskView object
        return f(self, user, *args, **kwargs)
    return wrapper


def view_requires_auth(permission=''):
    """
    Decorator to require Authorization and specific permissions for a given route
    :param permission: permissions required for wrapped route
    :return: double wrapped route return
    """
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            try:
                # it should use the get_token_auth_header method to get the token
                token = get_token_auth_header()
                # it should use the verify_decode_jwt method to decode the jwt
                payload = verify_decode_jwt(token)
                # it should use the check_permissions method validate claims and check the requested permission
                payload['token'] = token
                check_permissions(permission, payload)
            except AuthError as e:
                abort(make_response(jsonify(e.error), e.status_code))
            # self is a FlaskView object
            return f(self, payload, *args, **kwargs)
        return wrapper
    # return the decorator which passes the decoded payload to the decorated method
    return requires_auth_decorator


def requires_sign_in(f):
    """
    Decorator to require Authorization for a given route without any specific permissions
    :param f: function to wrap
    :return: function with wrapper
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            payload['token'] = token
            user = verify_user(payload)
            if current_user.is_anonymous:
                log.debug(f'signing in user: {profile.alternate_id}')
                login_user(user)
            elif current_user.alternate_id != user.alternate_id:
                raise AuthError({
                    'code': 'client_session_already_bound',
                    'description': 'Session already bound to different user credentials.'
                }, 401)
        except AuthError as e:
            abort(make_response(jsonify(e.error), e.status_code))
        return f(user, *args, **kwargs)
    return wrapper

'''
def requires_auth(permission=''):
    """
    Decorator to require Authorization and specific permissions for a given route
    :param permission: permissions required for wrapped route
    :return: double wrapped route return
    """
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                # it should use the get_token_auth_header method to get the token
                token = get_token_auth_header()
                # it should use the verify_decode_jwt method to decode the jwt
                payload = verify_decode_jwt(token)
                # it should use the check_permissions method validate claims and check the requested permission
                payload['token'] = token
                check_permissions(permission, payload)
            except AuthError as e:
                abort(make_response(jsonify(e.error), e.status_code))
            return f(payload, *args, **kwargs)
        return wrapper
    # return the decorator which passes the decoded payload to the decorated method
    return requires_auth_decorator
'''


