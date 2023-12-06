from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse
from django_quill.fields import QuillField

from killay.pages.lib.constants import PageConstants
from killay.admin.utils import InSiteManager


class Page(models.Model):
    title = models.CharField(
        verbose_name=PageConstants.FIELD_TITLE,
        help_text=PageConstants.FIELD_TITLE_HELP_TEXT,
        max_length=150,
        null=False,
        blank=False,
    )
    slug = models.SlugField(
        verbose_name=PageConstants.FIELD_SLUG,
        help_text=PageConstants.FIELD_SLUG_HELP_TEXT,
        max_length=150,
        null=False,
        blank=False,
    )
    kind = models.CharField(
        verbose_name=PageConstants.FIELD_KIND,
        help_text=PageConstants.FIELD_KIND_HELP_TEXT,
        choices=PageConstants.KIND_CHOICES,
        max_length=10,
        default=PageConstants.KIND_PAGE,
    )
    created_at = models.DateTimeField(
        verbose_name=PageConstants.FIELD_CREATED_AT,
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=PageConstants.FIELD_UPDATED_AT, auto_now=True
    )
    is_visible = models.BooleanField(
        verbose_name=PageConstants.FIELD_IS_VISIBLE,
        help_text=PageConstants.FIELD_IS_VISIBLE_HELP_TEXT,
        default=False,
    )
    body = QuillField(
        verbose_name=PageConstants.FIELD_BODY,
        help_text=PageConstants.FIELD_BODY_HELP_TEXT,
        null=True,
        blank=True,
    )
    header_image = models.ImageField(
        verbose_name=PageConstants.FIELD_HEADER_IMAGE,
        help_text=PageConstants.FIELD_HEADER_IMAGE_HELP_TEXT,
        upload_to="page_images",
        null=True,
        blank=True,
    )
    redirect_to = models.URLField(
        verbose_name=PageConstants.FIELD_REDIRECT_TO,
        help_text=PageConstants.FIELD_REDIRECT_TO_HELP_TEXT,
        null=True,
        blank=True,
    )
    position = models.PositiveSmallIntegerField(
        verbose_name=PageConstants.FIELD_POSITION,
        help_text=PageConstants.FIELD_POSITION_HELP_TEXT,
        default=0,
    )
    archive = models.ForeignKey(
        "archives.Archive",
        verbose_name=PageConstants.FIELD_ARCHIVE,
        help_text=PageConstants.FIELD_ARCHIVE_HELP_TEXT,
        on_delete=models.SET_NULL,
        related_name="pages",
        null=True,
        blank=True,
    )
    collection = models.ForeignKey(
        "archives.Collection",
        verbose_name=PageConstants.FIELD_COLLECTION,
        help_text=PageConstants.FIELD_COLLECTION_HELP_TEXT,
        on_delete=models.SET_NULL,
        related_name="pages",
        null=True,
        blank=True,
    )
    place = models.ForeignKey(
        "archives.Place",
        verbose_name=PageConstants.FIELD_PLACE,
        help_text=PageConstants.FIELD_PLACE_HELP_TEXT,
        on_delete=models.SET_NULL,
        related_name="pages",
        null=True,
        blank=True,
    )
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name="pages", default=settings.SITE_ID
    )

    is_visible_in_navbar = models.BooleanField(
        verbose_name=PageConstants.FIELD_IS_VISIBLE_IN_NAVBAR,
        help_text=PageConstants.FIELD_IS_VISIBLE_IN_NAVBAR_HELP_TEXT,
        default=False,
    )
    is_visible_in_footer = models.BooleanField(
        verbose_name=PageConstants.FIELD_IS_VISIBLE_IN_FOOTER,
        help_text=PageConstants.FIELD_IS_VISIBLE_IN_FOOTER_HELP_TEXT,
        default=False,
    )
    is_title_visible_in_body = models.BooleanField(
        verbose_name=PageConstants.FIELD_IS_TITLE_VISIBLE_IN_BODY,
        help_text=PageConstants.FIELD_IS_TITLE_VISIBLE_IN_BODY_HELP_TEXT,
        default=False,
    )

    class Meta:
        unique_together = ["slug", "site"]
        verbose_name = PageConstants.VERBOSE_NAME
        verbose_name_plural = PageConstants.VERBOSE_NAME_PLURAL
        ordering = ["position"]

    objects = models.Manager()
    objects_in_site = InSiteManager()

    def __str__(self):
        return f"{self.title} <{self.slug}>"

    def get_absolute_url(self):
        if self.kind == PageConstants.KIND_LINK:
            return self.redirect_to
        return reverse("pages:detail", kwargs={"slug": self.slug})

    @property
    def is_home(self):
        return self.slug == "home"
