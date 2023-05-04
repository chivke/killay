from django.db import models
from django.utils.translation import gettext_lazy


class TimeBase(models.Model):
    created_at = models.DateTimeField(gettext_lazy("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(gettext_lazy("Updated at"), auto_now=True)

    class Meta:
        abstract = True


class CategorizationBase(models.Model):
    name = models.CharField(
        gettext_lazy("Name"), max_length=255, null=False, blank=False
    )
    slug = models.SlugField(
        gettext_lazy("Slug"), max_length=255, null=False, blank=False, db_index=True
    )
    description = models.TextField(gettext_lazy("Description"), null=True, blank=True)
    position = models.PositiveSmallIntegerField(gettext_lazy("Position"), default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name} <{self.slug}>"


class SequenceManager(models.Manager):
    def get_ordered_data(self):
        return [
            {
                "order": index + 1,
                **sequence.__dict__,
                "ini_sec": sequence.ini_sec,
                "end_sec": sequence.end_sec,
            }
            for index, sequence in enumerate(self.all())
        ]
