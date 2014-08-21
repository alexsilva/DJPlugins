from django.utils import importlib


def exists(app_module):
    """
     check if the app exists in path
    :param name:
    """
    try:
        app = importlib.import_module(app_module)
    except ImportError:
        app = None
    return app is not None