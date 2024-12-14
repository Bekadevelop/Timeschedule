from django.apps import AppConfig

class UuserConfig(AppConfig):
    name = 'uuser'

    def ready(self):
        import uuser.signals
