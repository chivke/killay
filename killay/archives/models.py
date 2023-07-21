from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import gettext_lazy

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
    image = models.ImageField(
        gettext_lazy("Image"), upload_to="archive_images", null=True
    )

    class Meta:
        verbose_name = gettext_lazy("archive")
        verbose_name_plural = gettext_lazy("archives")
        ordering = ["position", "name"]

    objects = models.Manager()
    objects_in_site = InSiteManager()
    is_visible = models.BooleanField(default=True)
    is_restricted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} <{self.slug}>"


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
    is_restricted = models.BooleanField(default=False)
    image = models.ImageField(
        gettext_lazy("Image"), upload_to="collection_images", null=True
    )

    class Meta:
        verbose_name = gettext_lazy("collection")
        verbose_name_plural = gettext_lazy("collections")
        ordering = ["position", "slug"]
        unique_together = ["slug", "site"]

    objects = models.Manager()
    objects_in_site = InSiteManager()

    def __str__(self):
        return f"{self.name} <{self.slug}>"

    @property
    def archive_slug(self):
        return self.archive.slug


class Category(TimeBase, CategorizationBase):
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="categories",
        default=settings.SITE_ID,
    )
    collection = models.ForeignKey(
        Collection,
        on_delete=models.SET_NULL,
        related_name="categories",
        null=True,
    )

    class Meta:
        verbose_name = gettext_lazy("category")
        verbose_name_plural = gettext_lazy("categories")
        ordering = ["position", "slug"]
        unique_together = ["slug", "site"]

    objects = models.Manager()
    objects_in_site = InSiteManager()

    def __str__(self):
        return self.name

    @property
    def collection_slug(self):
        return self.collection.slug

    @property
    def archive_slug(self):
        return self.collection.archive.slug


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
        return self.name


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
        return self.name


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
    is_restricted = models.BooleanField(default=False)

    class Meta:
        verbose_name = gettext_lazy("piece")
        verbose_name_plural = gettext_lazy("pieces")
        ordering = ["title", "code"]
        unique_together = ["code", "site"]

    objects = models.Manager()
    objects_in_site = InSiteManager()

    def __str__(self):
        return f"Piece <{self.code}>"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            self.meta
        except PieceMeta.DoesNotExist:
            self.meta, _ = PieceMeta.objects.get_or_create(piece_id=self.pk)

    @property
    def active_provider(self) -> "Provider":
        return self.providers.filter(active=True).first()


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
    image = models.ImageField(
        gettext_lazy("Image"), upload_to="piece_images", null=True
    )
    file = models.FileField(gettext_lazy("File"), upload_to="piece_files", null=True)

    class Meta:
        verbose_name = gettext_lazy("video provider")
        verbose_name_plural = gettext_lazy("video provider")
        ordering = ["plyr_provider"]

    def __str__(self):
        return f"Provider <{self.ply_embed_id}, {self.plyr_provider}>"

    def save(self, *args, **kwargs):
        if self.active:
            other_providers = self._get_related_providers()
            other_providers.update(active=False)
        super().save(*args, **kwargs)

    def _get_related_providers(self):
        return self.__class__.objects.filter(piece_id=self.piece_id).exclude(id=self.id)

    @property
    def video_url(self):
        template = ProviderConstants.URL_TEMPLATE[self.plyr_provider]
        return template.format(
            plyr_provider=self.plyr_provider,
            ply_embed_id=self.ply_embed_id,
        )

    @property
    def video_url_for_plyr(self):
        template = ProviderConstants.URL_PLYR_TEMPLATE[self.plyr_provider]
        return template.format(
            plyr_provider=self.plyr_provider,
            ply_embed_id=self.ply_embed_id,
        )

    @property
    def is_ready(self) -> bool:
        piece_kind = self.piece.kind
        if piece_kind == PieceConstants.KIND_VIDEO and not (
            self.plyr_provider and self.ply_embed_id
        ):
            return False
        elif piece_kind == PieceConstants.KIND_IMAGE and not self.image:
            return False
        elif (
            piece_kind
            in [
                PieceConstants.KIND_SOUND,
                PieceConstants.KIND_DOCUMENT,
            ]
            and not self.file
        ):
            return False
        return self.active


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


class Place(TimeBase):
    name = models.CharField(
        gettext_lazy("Name"), max_length=500, null=False, blank=False
    )
    allowed_pieces = models.ManyToManyField(
        Piece,
        related_name="allowed_places",
        verbose_name=gettext_lazy("Allowed Places"),
    )
    allowed_collections = models.ManyToManyField(
        Collection,
        related_name="allowed_places",
        verbose_name=gettext_lazy("Allowed Places"),
    )
    allowed_archives = models.ManyToManyField(
        Archive,
        related_name="allowed_places",
        verbose_name=gettext_lazy("Allowed Places"),
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="places",
        default=settings.SITE_ID,
    )
    objects = models.Manager()
    objects_in_site = InSiteManager()

    class Meta:
        verbose_name = gettext_lazy("place")
        verbose_name_plural = gettext_lazy("places")
        ordering = ["name"]

    def __str__(self):
        return f"Place <{self.name}>"


class PlaceAddress(TimeBase):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="addresses")
    ipv4 = models.GenericIPAddressField(
        gettext_lazy("IP Address"),
        unique=True,
        null=False,
        blank=False,
        db_index=True,
    )
    description = models.CharField(
        gettext_lazy("Description"), max_length=500, null=True, blank=True
    )

    class Meta:
        verbose_name = gettext_lazy("address")
        verbose_name_plural = gettext_lazy("addresses")
        ordering = ["ipv4"]

    def __str__(self):
        return f"PlaceAddress <{self.ipv4}>"
