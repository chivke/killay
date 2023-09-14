from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


from killay.viewer.lib.constants import ViewerConstants


class Viewer(models.Model):
    configuration = models.OneToOneField(
        "admin.SiteConfiguration",
        on_delete=models.CASCADE,
        related_name="viewer",
    )
    scope = models.CharField(
        ViewerConstants.NAME_SCOPE,
        choices=ViewerConstants.SCOPE_CHOICES,
        max_length=50,
        default=ViewerConstants.SCOPE_ALL,
        help_text=ViewerConstants.HELP_TEXT_SCOPE,
    )
    scope_archive = models.ForeignKey(
        "archives.Archive",
        on_delete=models.SET_NULL,
        related_name="viewer",
        help_text=ViewerConstants.HELP_TEXT_SCOPE_ARCHIVE,
        null=True,
    )
    scope_collection = models.ForeignKey(
        "archives.Collection",
        on_delete=models.SET_NULL,
        related_name="viewer",
        help_text=ViewerConstants.HELP_TEXT_SCOPE_COLLECTION,
        null=True,
    )
    home = models.CharField(
        ViewerConstants.NAME_HOME,
        choices=ViewerConstants.HOME_CHOICES,
        max_length=50,
        help_text=ViewerConstants.HELP_TEXT_HOME,
        default=ViewerConstants.HOME_DEFAULT,
    )
    home_page = models.ForeignKey(
        "pages.Page",
        on_delete=models.SET_NULL,
        help_text=ViewerConstants.HELP_TEXT_HOME_PAGE,
        related_name="viewer",
        null=True,
    )


class ContentStats(models.Model):
    viewer = models.ForeignKey(
        Viewer,
        on_delete=models.CASCADE,
        related_name="content_stats",
        null=True,
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_id")
    views = models.PositiveIntegerField(default=0)
