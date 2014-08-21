from django.db import models


class App(models.Model):
    name = models.CharField("Application Name", max_length=255)

    prefix = models.CharField("Regex Path", max_length=128)

    def __unicode__(self):
        return self.name