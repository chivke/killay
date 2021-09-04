from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy

from django.contrib.sites.models import Site


class PageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(site_id=settings.SITE_ID)


class Page(models.Model):
    title = models.CharField(
        gettext_lazy("Title"), max_length=150, null=False, blank=False
    )
    slug = models.SlugField(
        gettext_lazy("Slug"), max_length=150, null=False, blank=False
    )
    body = models.TextField(gettext_lazy("Body"), null=True, blank=True)
    is_visible = models.BooleanField(gettext_lazy("Is visible"), default=False)
    is_visible_in_navbar = models.BooleanField(
        gettext_lazy("Is visible in navbar"), default=False
    )
    is_visible_in_footer = models.BooleanField(
        gettext_lazy("Is visible in footer"), default=False
    )
    header_image = models.ImageField(
        gettext_lazy("Header mage"), upload_to="page_images", null=True, blank=True
    )
    created_at = models.DateTimeField(gettext_lazy("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(gettext_lazy("Updated at"), auto_now=True)
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name="pages", default=settings.SITE_ID
    )

    class Meta:
        unique_together = ["slug", "site"]
        verbose_name = gettext_lazy("page")
        verbose_name_plural = gettext_lazy("pages")

    objects = PageManager()

    def __str__(self):
        return f"{self.title} <{self.slug}>"

    def get_absolute_url(self):
        if self.is_home:
            return reverse("home")
        return reverse("pages:detail", kwargs={"slug": self.slug})

    @property
    def is_home(self):
        return self.slug == "home"
