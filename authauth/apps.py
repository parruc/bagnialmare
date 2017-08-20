from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'authauth'
    def ready(self):
        from authauth import signals; signals #pyflakes
