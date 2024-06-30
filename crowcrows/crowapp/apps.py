from django.apps import AppConfig


class CrowappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crowapp'

    def ready(self):
        import crowapp.signals
