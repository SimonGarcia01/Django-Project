from django.apps import AppConfig


class TemplatetagsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'templatetags'

    def ready(self):
        import templatetags.custom_tags  # noqa
