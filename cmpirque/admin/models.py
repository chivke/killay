from django.conf import settings
from django.db import models

from cmpirque.admin.lib.constants import AdminConfigurationConstants


class AdminConfigurationManager(models.Manager):
    def current(self):
        return self.filter(active=True).first()


class AdminConfiguration(models.Model):
    site_name = models.CharField(max_length=150, default=settings.SITE_NAME)
    active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)

    objects = AdminConfigurationManager()


class SocialMedia(models.Model):
    config = models.ForeignKey(
        AdminConfiguration, on_delete=models.CASCADE, related_name="social_medias"
    )
    provider = models.CharField(
        choices=AdminConfigurationConstants.PROVIDER_CHOICES,
        max_length=150,
        null=False,
        blank=False,
    )
    url = models.URLField()
    css_class = models.CharField(max_length=150, null=True, blank=True)
    is_visible = models.BooleanField(default=False)
