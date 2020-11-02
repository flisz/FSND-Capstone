import json


from .mixins.base import BaseView

from flask_login import login_user, logout_user, current_user, login_required
from flask import redirect, url_for, flash, session, request, render_template, jsonify

from mymed.setup.loggers import LOGGERS
from mymed.app.login import verify_user
from mymed.app.auth import view_requires_sign_in, get_cookie_session_token, AuthError, verify_decode_jwt

__all__ = ('AuthView',)

log = LOGGERS.Auth


AUTH0_DOMAIN = 'flis.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffee'
CLIENT_ID = 'I12UnrxbhRGHcQG9wCyJwARE3YN81WLz'  # the client id generated for the auth0 app
CALLBACK_URL = 'http://127.0.0.1:5000/auth/callback/'  # the url of the callback service


class AuthView(BaseView):
    def login(self):
        if current_user.is_anonymous:
            link = f'https://{AUTH0_DOMAIN}/authorize' \
                   f'?audience={API_AUDIENCE}' \
                   f'&response_type=token' \
                   f'&client_id={CLIENT_ID}' \
                   f'&redirect_uri={CALLBACK_URL}'
            return redirect(link)
        else:
            flash('I redirected over here')
            return redirect(url_for('RootView:profile'))

    @login_required
    def logout(self):
        log.debug(f'trying log out')
        logout_user()
        return render_template('pages/logout_callback.html')

    def callback(self):
        log.debug(f'made it to the callback!')
        if current_user.is_anonymous:
            return render_template('pages/login_callback.html')
        else:
            log.debug(f'already logged in!')
            return redirect(url_for('RootView:index'))

    @view_requires_sign_in
    def finalize(self, payload=None):
        log.debug(f'made it to the finalizer!')
        if not current_user.is_anonymous:
            log.debug(f'already logged in!')
        elif payload:
            flash('I can log you in now!')
            user = verify_user(payload)
            login_user(user)
        return jsonify({'success': True,
                        'redirect_url': url_for('RootView:index')})
