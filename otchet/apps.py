from django.apps import AppConfig
from threading import Thread
from threading import Lock

class OtchetConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'otchet'

    def ready(self):
        from . import updater
        updater.scheduler.start()
