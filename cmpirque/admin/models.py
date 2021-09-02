from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import gettext_lazy

from cmpirque.admin.lib.constants import SiteConfigurationConstants


class SiteConfigurationManager(models.Manager):
    def current(self):
        return self.filter(id=settings.SITE_ID).first()


class SiteConfiguration(models.Model):
    name = models.CharField(
        gettext_lazy("Name of Site"), max_length=250, default=settings.SITE_NAME
    )
    domain = models.CharField(
        gettext_lazy("Domain"), max_length=250, default=settings.SITE_DOMAIN
    )
    is_published = models.BooleanField(gettext_lazy("Is published"), default=True)

    class Meta:
        verbose_name = gettext_lazy("Site Configuration")

    objects = SiteConfigurationManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        site = self.get_site()
        site.name = self.name
        site.domain = self.domain
        site.save()

    def get_site(self):
        return Site.objects.get(id=self.id)


class SocialMedia(models.Model):
    config = models.ForeignKey(
        SiteConfiguration, on_delete=models.CASCADE, related_name="social_medias"
    )
    provider = models.CharField(
        verbose_name=gettext_lazy("Provider"),
        choices=SiteConfigurationConstants.PROVIDER_CHOICES,
        max_length=150,
        null=False,
        blank=False,
    )
    url = models.URLField(gettext_lazy("URL"))
    css_class = models.CharField(
        gettext_lazy("CSS Class"), max_length=150, null=True, blank=True
    )
    is_visible = models.BooleanField(gettext_lazy("Is visible"), default=False)
