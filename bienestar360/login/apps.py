from django.apps import AppConfig

class LoginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'login'

    def ready(self):
        from django.db.models.signals import post_migrate
        from .signals import create_initial_data
        post_migrate.connect(create_initial_data, sender=self)