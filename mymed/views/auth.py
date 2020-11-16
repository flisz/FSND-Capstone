import json


from .mixins.base import BaseView

from flask_login import login_user, logout_user, current_user, login_required
from flask import redirect, url_for, flash, session, request, render_template, jsonify, current_app

from mymed.setup.loggers import LOGGERS
from mymed.app.login import verify_user
from mymed.app.auth import view_requires_sign_in, get_cookie_session_token, AuthError, verify_decode_jwt

__all__ = ('AuthView',)

log = LOGGERS.Auth


class AuthView(BaseView):
    def login(self):
        if current_user.is_anonymous:
            auth0_domain = current_app.config['SETUP'].AUTH0_DOMAIN
            api_audience = current_app.config['SETUP'].AUTH0_API_AUDIENCE
            client_id = current_app.config['SETUP'].AUTH0_CLIENT_ID
            callback_url = current_app.config['SETUP'].AUTH0_CALLBACK_URL

            link = f'https://{auth0_domain}/authorize' \
                   f'?audience={api_audience}' \
                   f'&response_type=token' \
                   f'&client_id={client_id}' \
                   f'&redirect_uri={callback_url}'
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
    def finalize(self, user=None):
        log.debug(f'made it to the finalizer!')
        flash('Login Successful!')
        return jsonify({'success': True,
                        'redirect_url': url_for('RootView:index')})
