from django.conf import settings
from django.db import models


class AdminConfiguration(models.Model):
    site_name = models.CharField(max_length=150, default=settings.SITE_NAME)
    active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)


class SocialMedia(models.Model):
    config = models.ForeignKey(
        AdminConfiguration, on_delete=models.CASCADE, related_name="social_medias"
    )
    name = models.CharField(max_length=150)
    url = models.URLField()
    css_class = models.CharField(max_length=150, null=True, blank=True)
    is_visible = models.BooleanField(default=False)
