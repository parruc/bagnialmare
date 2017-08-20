from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'bagni'
    def ready(self):
        from bagni import search; search #pyflakes
        from bagni import signals; signals #pyflakes
