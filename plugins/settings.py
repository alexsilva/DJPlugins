
## Plugins settings
from plugins.models import App
from plugins.validate import exists
import logging, os


class Settings(object):
    """
    Modeling system configuration plugins.
    """
    logger_name = "plugins.apps.debug"
    logger_filename = logger_name.replace(".","_") + ".log"

    def __init__(self, _locals):
        self._locals = _locals

    def __call__(self, _locals):
        self._locals = _locals

    @classmethod
    def get_logger_name(cls):
        return cls.logger_name

    @property
    def logger(self):
        return logging.getLogger(self.logger_name)

    def set_installeds_apps(self):
        """
        Installed apps settings
        """
        for app in App.objects.all():
            if exists(app.name):
                self.logger.debug("settings::installed app %s"%app)
                self._locals["INSTALLED_APPS"] += (app.name, )
            else:
                self.logger.debug("settings::installed app not found %s"%app)

    def set_urlpatterns(self):
        """
        Url patterns settings
        """
        for app in App.objects.all():
            if exists(app.name):
                self.logger.debug("URLS: regex-pattern::add %s"%app)

                self._locals["urlpatterns"] += self._locals["patterns"]('',
                    self._locals["url"](app.prefix, self._locals["include"](app.name + ".urls")),
                )
            else:
                self.logger.debug("URLS: regex-pattern::app not found %s"%app)

    def set_loggins(self, path=''):
        self._locals['LOGGING']['loggers'][self.logger_name] = {
            'handlers': [],
            'level': 'DEBUG',
            'propagate': True,
            'filename': os.path.join(path, self.logger_filename)
        }