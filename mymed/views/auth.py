from .mixins.base import BaseView

from flask_login import login_user, logout_user, current_user
from flask import redirect, url_for, flash


__all__ = ('AuthView',)


class AuthView(BaseView):

    def login(self):
        if not current_user.is_anonymous:
            return redirect(url_for('RootView:index'))
        else:
            flash('I redirected over here')
            return redirect(url_for('RootView:index'))


    def logout(self):
        logout_user()
        return redirect(url_for('RootView:index'))


    def callback(self):
        if not current_user.is_anonymous:
            pass
        else:
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            if payload:
                pass
                # todo: get data out of payload to log-in user
            # todo: get user related to payload
            user = None
            if not user:
                pass
                # todo: add user to database
        redirect(url_for('RootView:index'))
