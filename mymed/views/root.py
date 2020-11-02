from flask import render_template, url_for
from flask_login import current_user, login_required
from .mixins.base import BaseView


__all__ = ('RootView',)


class RootView(BaseView):
    route_base = '/'

    def index(self):
        return render_template('pages/home.html', current_user=current_user)

    @login_required
    def profile(self, payload):
        return render_template('pages/home.html', current_user=current_user)

    def health(self):
        return "Healthy"
