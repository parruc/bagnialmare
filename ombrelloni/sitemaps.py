from django.utils.importlib import import_module

SITEMAPS = {}

def get_sitemaps(applications):
    _sitemaps = SITEMAPS
    for app in applications:
        app_package = import_module(app + ".sitemaps")
        _sitemaps.update(app_package.SITEMAPS)
    return _sitemaps

