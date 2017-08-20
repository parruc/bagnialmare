from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'booking'
    def ready(self):
        from booking import signals; signals #pyflakes
