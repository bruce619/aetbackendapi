from __future__ import unicode_literals
from django.apps import AppConfig


class MyapitestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapitest'

    def ready(self):
        import myapitest.signals