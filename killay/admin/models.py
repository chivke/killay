from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import gettext_lazy

from killay.admin.lib.constants import (
    LogoConstants,
    SiteConfigurationConstants,
    SocialMediaConstants,
)


class SiteConfigurationManager(models.Manager):
    def current(self):
        return self.filter(id=settings.SITE_ID).first()


class SiteConfiguration(models.Model):
    name = models.CharField(
        SiteConfigurationConstants.FIELD_NAME,
        help_text=SiteConfigurationConstants.FIELD_NAME_HELP_TEXT,
        max_length=250,
        default=settings.SITE_NAME,
        null=False,
        blank=False,
    )
    domain = models.CharField(
        SiteConfigurationConstants.FIELD_DOMAIN,
        help_text=SiteConfigurationConstants.FIELD_DOMAIN_HELP_TEXT,
        max_length=250,
        default=settings.SITE_DOMAIN,
        null=False,
        blank=False,
    )
    is_published = models.BooleanField(
        SiteConfigurationConstants.FIELD_IS_PUBLISHED,
        help_text=SiteConfigurationConstants.FIELD_IS_PUBLISHED_HELP_TEXT,
        default=True,
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="configuration",
        default=settings.SITE_ID,
    )
    footer_is_visible = models.BooleanField(
        SiteConfigurationConstants.FIELD_FOOTER_IS_VISIBLE,
        help_text=SiteConfigurationConstants.FIELD_FOOTER_IS_VISIBLE_HELP_TEXT,
        default=True,
    )
    collection_site = models.BooleanField(
        gettext_lazy("Collection site"), default=False
    )

    class Meta:
        verbose_name = SiteConfigurationConstants.VERBOSE_NAME

    objects = SiteConfigurationManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.site.name = self.name
        self.site.domain = self.domain
        self.site.save()


class SocialMediaManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset.filter(config__site_id=settings.SITE_ID)


class SocialMedia(models.Model):
    config = models.ForeignKey(
        SiteConfiguration, on_delete=models.CASCADE, related_name="social_medias"
    )
    provider = models.CharField(
        verbose_name=SocialMediaConstants.FIELD_PROVIDER,
        choices=SiteConfigurationConstants.PROVIDER_CHOICES,
        help_text=SocialMediaConstants.FIELD_PROVIDER_HELP_TEXT,
        max_length=150,
        null=False,
        blank=False,
    )
    url = models.URLField(
        SocialMediaConstants.FIELD_URL,
        help_text=SocialMediaConstants.FIELD_URL_HELP_TEXT,
    )
    is_visible = models.BooleanField(
        SocialMediaConstants.FIELD_IS_VISIBLE,
        help_text=SocialMediaConstants.FIELD_IS_VISIBLE_HELP_TEXT,
        default=False,
    )
    position = models.PositiveSmallIntegerField(
        SocialMediaConstants.FIELD_POSITION,
        help_text=SocialMediaConstants.FIELD_POSITION_HELP_TEXT,
        default=0,
    )

    class Meta:
        verbose_name = SocialMediaConstants.VERBOSE_NAME
        verbose_name_plural = SocialMediaConstants.VERBOSE_NAME_PLURAL
        ordering = ["position"]

    objects = models.Manager()
    objects_in_site = SocialMediaManager()


class LogoManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset.filter(configuration__site_id=settings.SITE_ID)


class Logo(models.Model):
    configuration = models.ForeignKey(
        SiteConfiguration, on_delete=models.CASCADE, related_name="logos"
    )
    name = models.CharField(
        LogoConstants.FIELD_NAME,
        help_text=LogoConstants.FIELD_NAME_HELP_TEXT,
        max_length=255,
    )
    image = models.ImageField(
        LogoConstants.FIELD_IMAGE,
        help_text=LogoConstants.FIELD_IMAGE_HELP_TEXT,
        upload_to="logos",
    )
    is_visible = models.BooleanField(
        LogoConstants.FIELD_IS_VISIBLE,
        help_text=LogoConstants.FIELD_IS_VISIBLE_HELP_TEXT,
        default=False,
    )
    position = models.PositiveSmallIntegerField(
        LogoConstants.FIELD_POSITION,
        help_text=LogoConstants.FIELD_POSITION_HELP_TEXT,
        default=0,
    )

    class Meta:
        verbose_name = LogoConstants.VERBOSE_NAME
        verbose_name_plural = LogoConstants.VERBOSE_NAME_PLURAL
        ordering = ["position"]

    objects = models.Manager()
    objects_in_site = LogoManager()
