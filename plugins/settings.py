
## Plugins settings
from plugins.models import App
from plugins.validate import exists
import logging
import os


class Settings(object):
    """
    Modeling system configuration plugins.
    """
    logger_name = "plugins.apps.debug"
    logger_filename = logger_name.replace(".","_") + ".log"

    def __init__(self, _locals):
        self._locals = _locals

    def set_installeds_apps(self):
        """
        Installed apps settings
        """
        logger = logging.getLogger(self.logger_name)

        for app in App.objects.all():
            if exists(app.name):
                logger.debug("settings::installed app %s"%app)
                self._locals["INSTALLED_APPS"] += (app.name, )
            else:
                logger.debug("settings::installed app not found %s"%app)

    def set_loggins(self, path=''):
        self._locals['LOGGING']['loggers'][self.logger_name] = {
            'handlers': [],
            'level': 'DEBUG',
            'propagate': True,
            'filename': os.path.join(path, self.logger_filename)
        }