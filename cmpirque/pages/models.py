from django.db import models
from django.urls import reverse


class Page(models.Model):
    """Model for pages with static content."""
    title = models.CharField(max_length=100, null=False, blank=False)
    slug = models.SlugField(null=False, blank=False)
    body = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} <{self.slug}>"

    def get_absolute_url(self):
        if self.slug == "home":
            return reverse("home")
        return reverse("pages:detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'page'
        verbose_name_plural = 'pages'