
def exists(name):
    """
     check if the app exists in path
    :param name:
    """
    try:
        app = __import__(name)
    except ImportError as err:
        app = None
    return app is not None