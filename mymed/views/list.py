from .mixins.base import BaseView


__all__ = ('ListView',)


class ListView(BaseView):
    def index(self):
        return "Hello"

    def health(self):
        return "Healthy"

