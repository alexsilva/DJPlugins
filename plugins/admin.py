import sys
import logging

from django.contrib import admin
from django.contrib.admin import site
from django.conf import settings
from django.utils import importlib

from plugins.models import App
from plugins.validate import exists


class AppAdmin(admin.ModelAdmin):
    logger = logging.getLogger(settings.PLUGIN_SETTINGS.get_logger_name())

    @classmethod
    def force_url_conf_reload(cls):
        """
        Remove the url conf standard sys.module makes the url patterns are
        recharged and the urls of the app (plugin) are recognized at runtime.
        """
        if settings.ROOT_URLCONF in sys.modules:
            url_conf = sys.modules[settings.ROOT_URLCONF]
        else:
            url_conf = importlib.import_module(settings.ROOT_URLCONF)

        # configuring the object
        settings.PLUGIN_SETTINGS(url_conf.__dict__)

        # urls patterns settings
        settings.PLUGIN_SETTINGS.set_urlpatterns()

        cls.logger.info('urlpatterns: %s' % url_conf.__dict__['urlpatterns'])

    def add_configure(self, obj):
        if exists(obj.name) and not obj.name in settings.INSTALLED_APPS:
            self.logger.debug("MODEL: settings::installed-app " + obj.name)
            settings._wrapped.INSTALLED_APPS += (obj.name, )  # hardcore change!
        else:
            self.logger.debug("MODEL: settings::installed-app " + obj.name)

        # Force reloading the url conf standard.
        self.force_url_conf_reload()

    def del_configure(self, obj):
        if obj.name in settings.INSTALLED_APPS:
            self.logger.debug("MODEL: settings::delete-app " + obj.name)

            apps = list(settings.INSTALLED_APPS)
            apps.remove(obj.name)

            settings._wrapped.INSTALLED_APPS = apps  # hardcore change!
        else:
            self.logger.debug("MODEL: settings::delete-app fail " + obj.name)

        # Force reloading the url conf standard.
        self.force_url_conf_reload()

    def save_model(self, request, obj, form, change):
        super(AppAdmin, self).save_model(request, obj, form, change)

        if not change: self.add_configure(obj)

    def delete_model(self, request, obj):
        super(AppAdmin, self).delete_model(request, obj)

        self.del_configure(obj)

site.register(App, AppAdmin)