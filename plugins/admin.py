from django.contrib import admin
from django.contrib.admin import site
from plugins.models import App

from django.conf import settings
from plugins.validate import app_exists


class AppAdmin(admin.ModelAdmin):

    def add_configure(self, obj):
        if app_exists(obj.name) and not obj.name in settings.INSTALLED_APPS:
            print "LOG: settings::add "+obj.name
            settings._wrapped.INSTALLED_APPS += (obj.name, ) # hardcore change!
        else:
            print "LOG: settings::add fail"
            for name in settings.INSTALLED_APPS:
                print name

    def del_configure(self, obj):
        if obj.name in settings.INSTALLED_APPS:
            print "LOG: settings::delete "+obj.name

            apps = list(settings.INSTALLED_APPS)
            apps.remove( obj.name )

            settings._wrapped.INSTALLED_APPS = apps # hardcore change!
        else:
            print "LOG: settings::delete fail"

    def save_model(self, request, obj, form, change):
        super(AppAdmin,self).save_model(request, obj, form, change)

        if not change: self.add_configure( obj )

    def delete_model(self, request, obj):
        super(AppAdmin,self).delete_model(request, obj)

        self.del_configure( obj )

# --------------------------------------------------------------------------
site.register(App, AppAdmin)