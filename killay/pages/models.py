from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy
from django_quill.fields import QuillField

from killay.pages.lib.constants import PageConstants
from killay.admin.utils import InSiteManager


class Page(models.Model):
    title = models.CharField(
        PageConstants.NAME_TITLE, max_length=150, null=False, blank=False
    )
    slug = models.SlugField(
        PageConstants.NAME_SLUG, max_length=150, null=False, blank=False
    )
    kind = models.CharField(
        verbose_name=PageConstants.NAME_KIND,
        choices=PageConstants.KIND_CHOICES,
        max_length=10,
        default=PageConstants.KIND_PAGE,
    )
    created_at = models.DateTimeField(PageConstants.NAME_CREATED_AT, auto_now_add=True)
    updated_at = models.DateTimeField(PageConstants.NAME_UPDATED_AT, auto_now=True)
    is_visible = models.BooleanField(PageConstants.NAME_IS_VISIBLE, default=False)
    body = QuillField(PageConstants.NAME_BODY, null=True, blank=True)
    header_image = models.ImageField(
        PageConstants.NAME_HEADER_IMAGE, upload_to="page_images", null=True, blank=True
    )
    redirect_to = models.URLField(PageConstants.NAME_REDIRECT_TO, null=True, blank=True)
    position = models.PositiveSmallIntegerField(PageConstants.NAME_POSITION, default=0)
    archive = models.ForeignKey(
        "archives.Archive",
        on_delete=models.SET_NULL,
        related_name="pages",
        null=True,
        blank=True,
    )
    collection = models.ForeignKey(
        "archives.Collection",
        on_delete=models.SET_NULL,
        related_name="pages",
        null=True,
        blank=True,
    )
    place = models.ForeignKey(
        "archives.Place",
        on_delete=models.SET_NULL,
        related_name="pages",
        null=True,
        blank=True,
    )
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name="pages", default=settings.SITE_ID
    )

    is_visible_in_navbar = models.BooleanField(
        gettext_lazy("Is visible in navbar"), default=False
    )
    is_visible_in_footer = models.BooleanField(
        gettext_lazy("Is visible in footer"), default=False
    )
    is_title_visible_in_body = models.BooleanField(
        gettext_lazy("Is title visible in body"), default=False
    )
    # to deprecate
    collection_site = models.ForeignKey(
        "videos.VideoCollection",
        on_delete=models.CASCADE,
        related_name="pages",
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ["slug", "site"]
        verbose_name = gettext_lazy("page")
        verbose_name_plural = gettext_lazy("pages")
        ordering = ["position"]

    objects = models.Manager()
    objects_in_site = InSiteManager()

    def __str__(self):
        return f"{self.title} <{self.slug}>"

    def get_absolute_url(self):
        if self.is_home:
            return reverse("home")
        elif self.kind == PageConstants.KIND_LINK:
            return self.redirect_to
        return reverse("pages:detail", kwargs={"slug": self.slug})

    @property
    def is_home(self):
        return self.slug == "home"
