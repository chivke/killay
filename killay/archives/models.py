from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import gettext_lazy
from django.urls import reverse

from killay.admin.utils import InSiteManager
from killay.archives.lib.constants import PieceConstants, ProviderConstants
from killay.archives.managers import CategorizationBase, SequenceManager, TimeBase


class Archive(TimeBase):
    name = models.CharField(
        gettext_lazy("Name"), max_length=255, null=False, blank=False
    )
    slug = models.SlugField(
        gettext_lazy("Slug"), max_length=255, unique=True, null=False, blank=False
    )
    description = models.TextField(gettext_lazy("Description"), null=True, blank=True)
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="archives",
        default=settings.SITE_ID,
    )
    position = models.PositiveSmallIntegerField(gettext_lazy("Position"), default=0)

    class Meta:
        verbose_name = gettext_lazy("archive")
        verbose_name_plural = gettext_lazy("archives")
        ordering = ["position", "name"]

    objects = models.Manager()
    objects_in_site = InSiteManager()

    def __str__(self):
        return f"{self.name} <{self.slug}>"

    def get_update_url(self):
        return reverse(
            "admin:archive_update",
            kwargs={"slug": self.slug},
        )


class Collection(TimeBase, CategorizationBase):
    archive = models.ForeignKey(
        Archive,
        on_delete=models.CASCADE,
        related_name="collections",
        null=False,
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="collections",
        default=settings.SITE_ID,
    )
    is_visible = models.BooleanField(default=True)

    class Meta:
        verbose_name = gettext_lazy("collection")
        verbose_name_plural = gettext_lazy("collections")
        ordering = ["position", "slug"]
        unique_together = ["slug", "site"]

    objects = models.Manager()
    objects_in_site = InSiteManager()

    def __str__(self):
        return f"{self.name} <{self.slug}>"

    def get_update_url(self):
        return reverse(
            "admin:collection_update",
            kwargs={"slug": self.slug},
        )


class Category(TimeBase, CategorizationBase):
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="categories",
        default=settings.SITE_ID,
    )

    class Meta:
        verbose_name = gettext_lazy("category")
        verbose_name_plural = gettext_lazy("categories")
        ordering = ["position", "slug"]
        unique_together = ["slug", "site"]

    objects = models.Manager()
    objects_in_site = InSiteManager()

    def __str__(self):
        return f"Category <{self.name}>"


class Person(TimeBase, CategorizationBase):
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="persons",
        default=settings.SITE_ID,
    )

    class Meta:
        verbose_name = gettext_lazy("person")
        verbose_name_plural = gettext_lazy("people")
        ordering = ["position", "slug"]
        unique_together = ["slug", "site"]

    objects = models.Manager()
    objects_in_site = InSiteManager()

    def __str__(self):
        return f"Person <{self.name}>"


class Keyword(TimeBase, CategorizationBase):
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="keywords",
        default=settings.SITE_ID,
    )

    class Meta:
        verbose_name = gettext_lazy("keyword")
        verbose_name_plural = gettext_lazy("keywords")
        ordering = ["position", "slug"]
        unique_together = ["slug", "site"]

    objects = models.Manager()
    objects_in_site = InSiteManager()

    def __str__(self):
        return f"Keyword <{self.name}>"


class Piece(TimeBase):
    code = models.SlugField(gettext_lazy("Code"), null=False, blank=False)
    title = models.CharField(
        gettext_lazy("Title"), max_length=512, null=False, blank=False
    )
    thumb = models.ImageField(
        gettext_lazy("Thumb"), upload_to="piece_thumbs", null=True, blank=True
    )
    is_published = models.BooleanField(gettext_lazy("Published"), default=False)
    kind = models.CharField(
        gettext_lazy("Kind"),
        choices=PieceConstants.KIND_CHOICES,
        max_length=50,
        null=False,
        blank=False,
    )
    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        related_name="pieces",
        null=False,
    )
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name="pieces", default=settings.SITE_ID
    )
    categories = models.ManyToManyField(
        "Category", related_name="pieces", verbose_name=gettext_lazy("Categories")
    )
    people = models.ManyToManyField(
        "Person", related_name="pieces", verbose_name=gettext_lazy("People")
    )
    keywords = models.ManyToManyField(
        "Keyword", related_name="pieces", verbose_name=gettext_lazy("Keywords")
    )

    class Meta:
        verbose_name = gettext_lazy("piece")
        verbose_name_plural = gettext_lazy("pieces")
        ordering = ["title", "code"]

    objects = models.Manager()
    objects_in_site = InSiteManager()

    def __str__(self):
        return f"Piece <{self.code}>"


class Sequence(TimeBase):
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name="sequences")
    title = models.CharField(
        gettext_lazy("Title"), max_length=500, null=True, blank=True
    )
    content = models.TextField(gettext_lazy("Content"), null=True, blank=True)
    ini = models.TimeField(gettext_lazy("Initiation"), null=False, blank=False)
    end = models.TimeField(gettext_lazy("End"), null=False, blank=False)

    class Meta:
        verbose_name = gettext_lazy("sequence")
        verbose_name_plural = gettext_lazy("sequences")
        ordering = ["ini"]

    objects = SequenceManager()

    @property
    def ini_sec(self):
        return self.__time_to_seconds(self.ini)

    @property
    def end_sec(self):
        return self.__time_to_seconds(self.end)

    def __time_to_seconds(self, time):
        return (time.hour * 60 + time.minute) * 60 + time.second

    def __str__(self):
        return f"Sequence <{self.id}>"


class Provider(models.Model):
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name="providers")
    active = models.BooleanField(gettext_lazy("Active"), default=False)
    online = models.BooleanField(gettext_lazy("Online"), default=False)
    checked_at = models.DateTimeField(gettext_lazy("Checked at"), null=True, blank=True)
    ply_embed_id = models.CharField(
        gettext_lazy("Ply Embed ID"), max_length=500, null=False, blank=False
    )
    plyr_provider = models.CharField(
        gettext_lazy("Ply Provider"),
        choices=ProviderConstants.PLYR_PROVIDER_CHOICES,
        max_length=50,
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = gettext_lazy("video provider")
        verbose_name_plural = gettext_lazy("video provider")

    def __str__(self):
        return f"Provider <{self.ply_embed_id}, {self.plyr_provider}>"


class PieceMeta(TimeBase):
    piece = models.OneToOneField(Piece, on_delete=models.CASCADE, related_name="meta")
    event = models.CharField(
        gettext_lazy("Event"), max_length=500, null=True, blank=True
    )
    description = models.TextField(gettext_lazy("Description"), null=True, blank=True)
    description_date = models.DateField(
        gettext_lazy("Description Date"), null=True, blank=True
    )
    location = models.CharField(
        gettext_lazy("Location"), max_length=500, null=True, blank=True
    )
    duration = models.TimeField(gettext_lazy("Duration"), null=True, blank=True)
    register_date = models.DateField(
        gettext_lazy("Register Date"), null=True, blank=True
    )
    register_author = models.CharField(
        gettext_lazy("Register Author"), max_length=500, null=True, blank=True
    )
    productor = models.CharField(
        gettext_lazy("Productor"), max_length=500, null=True, blank=True
    )
    notes = models.TextField(gettext_lazy("Notes"), null=True, blank=True)
    archivist_notes = models.TextField(
        gettext_lazy("Archivist Notes"), null=True, blank=True
    )
    documentary_unit = models.CharField(
        gettext_lazy("Documentary Unit"), max_length=500, null=True, blank=True
    )
    lang = models.CharField(
        gettext_lazy("Language"), max_length=500, null=True, blank=True
    )
    original_format = models.CharField(
        gettext_lazy("Original Format"), max_length=500, null=True, blank=True
    )

    class Meta:
        verbose_name = gettext_lazy("piece metadata")
        verbose_name_plural = gettext_lazy("piece metadatas")

    def __str__(self):
        return f"PieceMeta <of {self.piece_id}>"
