
## Plugins settings
from plugins.models import App
from plugins.validate import exists
import logging, os
# ---------------------------------------------------------------------------------
class Logger(object):
    """
    Class used in the construction of the log file of the application.
    """
    def __init__(self, name="plugins.apps.debug", filename=""):
        self._filename = (filename or (name.replace(".","_")+".log"))
        self._name = name
        self._log = None

    @property
    def name(self): return self._name
    @name.setter
    def name(self, n): self._name = n

    @property
    def filename(self): return self._filename
    @filename.setter
    def filename(self, fn): self._filename = fn

    @property
    def log(self):
        if self._log is None:
            self._log = logging.getLogger(self._name)
        return self._log

# ---------------------------------------------------------------------------------
class Settings(object):
    """
    Modeling system configuration plugins.
    """
    logger = Logger()

    def __init__(self, _locals):
        self._locals = _locals

    def __call__(self, _locals):
        self._locals = _locals

    @classmethod
    def get_logger_name(cls):
        return cls.logger.name

    @property
    def log(self):
        return self.logger.log

    def set_installeds_apps(self):
        """
        Installed apps settings
        """
        for app in App.objects.all():
            if exists(app.name):
                self.log.debug("settings::installed app %s"%app)
                self._locals["INSTALLED_APPS"] += (app.name, )
            else:
                self.log.debug("settings::installed app not found %s"%app)

    def set_urlpatterns(self):
        """
        Url patterns settings
        """
        from django.conf.urls import patterns, include, url

        for app in App.objects.all():
            if exists(app.name):
                self.log.debug("URLS: regex-pattern::add %s"%app)

                self._locals["urlpatterns"] += patterns('',
                    url(app.prefix, include(app.name + ".urls")),
                )
            else:
                self.log.debug("URLS: regex-pattern::app not found %s"%app)

    def set_loggins(self, path, name='', filename=''):
        """
        Log Settings application.

        :param name: Log name (optional).
        :param filename: Name of the log file (optional).
        :param path: Path of the log file.
        """
        self.logger.name = (name or self.logger.name)
        self.logger.filename = (filename or self.logger.filename)

        self._locals['LOGGING']['loggers'][self.logger.name] = {
            'handlers': [],
            'level': 'DEBUG',
            'propagate': True,
            'filename': os.path.join(path, self.logger.filename)
        }