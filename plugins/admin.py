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
    def update_urlconf(cls, *args):
        """
        Remove the url conf standard sys.module makes the url patterns are
        recharged and the urls of the app (plugin) are recognized at runtime.
        """
        if settings.ROOT_URLCONF in sys.modules:
            urlconf = sys.modules[settings.ROOT_URLCONF]
        else:
            urlconf = importlib.import_module(settings.ROOT_URLCONF)

        # configuring the object
        settings.PLUGIN_SETTINGS(urlconf.__dict__)

        # urls patterns settings
        settings.PLUGIN_SETTINGS.set_urlpatterns(*args)

    def after_save_model(self, obj):
        if exists(obj.name) and not obj.name in settings.INSTALLED_APPS:
            self.logger.debug("MODEL: settings::installed-app " + obj.name)
            # hardcore change!
            settings._wrapped.INSTALLED_APPS += (obj.name, )
        else:
            self.logger.debug("MODEL: settings::installed-app " + obj.name)

    def after_delete_model(self, obj):
        if obj.name in settings.INSTALLED_APPS:
            self.logger.debug("MODEL: settings::delete-app " + obj.name)

            apps = list(settings.INSTALLED_APPS)
            apps.remove(obj.name)

            # hardcore change!
            settings._wrapped.INSTALLED_APPS = apps
        else:
            self.logger.debug("MODEL: settings::delete-app fail " + obj.name)

    def save_model(self, request, obj, form, change):
        super(AppAdmin, self).save_model(request, obj, form, change)

        if not change:
            self.after_save_model(obj)

        # Force reloading the url conf standard.
        self.update_urlconf()

    def delete_model(self, request, obj):
        super(AppAdmin, self).delete_model(request, obj)

        self.after_delete_model(obj)

        # Force reloading the url conf standard.
        self.update_urlconf(obj)

site.register(App, AppAdmin)