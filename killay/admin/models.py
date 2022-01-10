from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import gettext_lazy

from killay.admin.lib.constants import SiteConfigurationConstants


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
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="configuration",
        default=settings.SITE_ID,
    )
    footer_is_visible = models.BooleanField(
        gettext_lazy("Footer is visible"), default=True
    )
    collection_site = models.BooleanField(
        gettext_lazy("Collection site"), default=False
    )

    class Meta:
        verbose_name = gettext_lazy("Site Configuration")

    objects = SiteConfigurationManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.site.name = self.name
        self.site.domain = self.domain
        self.site.save()


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
    is_visible = models.BooleanField(gettext_lazy("Is visible"), default=False)
    position = models.PositiveSmallIntegerField(gettext_lazy("Position"), default=0)

    class Meta:
        verbose_name = gettext_lazy("social media")
        verbose_name_plural = gettext_lazy("social medias")
        ordering = ["position"]


class Logo(models.Model):
    configuration = models.ForeignKey(
        SiteConfiguration, on_delete=models.CASCADE, related_name="logos"
    )
    name = models.CharField(gettext_lazy("Name"), max_length=255)
    image = models.ImageField(gettext_lazy("Image"), upload_to="logos")
    is_visible = models.BooleanField(gettext_lazy("Is visible"), default=False)
    position = models.PositiveSmallIntegerField(gettext_lazy("Position"), default=0)

    class Meta:
        verbose_name = gettext_lazy("logo")
        verbose_name_plural = gettext_lazy("logos")
        ordering = ["position"]
