from django.apps import AppConfig


class TransportAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transport_app'

    def ready(self):
        import transport_app.signals
