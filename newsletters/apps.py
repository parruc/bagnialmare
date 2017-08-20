from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'newsletter'
    def ready(self):
        from newsletter import signals; signals  # pyflakes
