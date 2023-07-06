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
        gettext_lazy("Title"), max_length=150, null=False, blank=False
    )
    slug = models.SlugField(
        gettext_lazy("Slug"), max_length=150, null=False, blank=False
    )
    kind = models.CharField(
        verbose_name=gettext_lazy("Provider"),
        choices=PageConstants.KIND_CHOICES,
        max_length=10,
        default=PageConstants.PAGE,
    )
    body = QuillField(gettext_lazy("Body"), null=True, blank=True)
    is_visible = models.BooleanField(gettext_lazy("Is visible"), default=False)
    is_visible_in_navbar = models.BooleanField(
        gettext_lazy("Is visible in navbar"), default=False
    )
    is_visible_in_footer = models.BooleanField(
        gettext_lazy("Is visible in footer"), default=False
    )
    is_title_visible_in_body = models.BooleanField(
        gettext_lazy("Is title visible in body"), default=False
    )
    header_image = models.ImageField(
        gettext_lazy("Header mage"), upload_to="page_images", null=True, blank=True
    )
    created_at = models.DateTimeField(gettext_lazy("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(gettext_lazy("Updated at"), auto_now=True)
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name="pages", default=settings.SITE_ID
    )
    position = models.PositiveSmallIntegerField(gettext_lazy("Position"), default=0)
    redirect_to = models.URLField(
        gettext_lazy("Redirect to (URL)"), null=True, blank=True
    )
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
        elif self.kind == PageConstants.LINK:
            return self.redirect_to
        return reverse("pages:detail", kwargs={"slug": self.slug})

    @property
    def is_home(self):
        return self.slug == "home"
