from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models

from killay.admin.utils import InSiteManager
from killay.archives.lib.constants import (
    ArchiveConstants,
    CategoryConstants,
    CollectionConstants,
    KeywordConstants,
    PersonConstants,
    PieceConstants,
    PieceMetaConstants,
    PlaceConstants,
    PlaceAddressConstants,
    ProviderConstants,
    SequenceConstants,
)
from killay.archives.managers import CategorizationBase, SequenceManager, TimeBase


class Archive(TimeBase):
    name = models.CharField(
        verbose_name=ArchiveConstants.FIELD_NAME,
        help_text=ArchiveConstants.FIELD_NAME_HELP_TEXT,
        max_length=255,
        null=False,
        blank=False,
    )
    slug = models.SlugField(
        verbose_name=ArchiveConstants.FIELD_SLUG,
        help_text=ArchiveConstants.FIELD_SLUG_HELP_TEXT,
        max_length=255,
        unique=True,
        null=False,
        blank=False,
    )
    description = models.TextField(
        verbose_name=ArchiveConstants.FIELD_DESCRIPTION,
        help_text=ArchiveConstants.FIELD_DESCRIPTION_HELP_TEXT,
        null=True,
        blank=True,
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="archives",
        default=settings.SITE_ID,
    )
    position = models.PositiveSmallIntegerField(
        verbose_name=ArchiveConstants.FIELD_POSITION,
        help_text=ArchiveConstants.FIELD_POSITION_HELP_TEXT,
        default=0,
    )
    image = models.ImageField(
        verbose_name=ArchiveConstants.FIELD_IMAGE,
        help_text=ArchiveConstants.FIELD_IMAGE_HELP_TEXT,
        upload_to="archive_images",
        null=True,
    )
    is_visible = models.BooleanField(
        verbose_name=ArchiveConstants.FIELD_IS_VISIBLE,
        help_text=ArchiveConstants.FIELD_IS_VISIBLE_HELP_TEXT,
        default=True,
    )
    is_restricted = models.BooleanField(
        verbose_name=ArchiveConstants.FIELD_IS_RESTRICTED,
        help_text=ArchiveConstants.FIELD_IS_RESTRICTED_HELP_TEXT,
        default=False,
    )

    class Meta:
        verbose_name = ArchiveConstants.VERBOSE_NAME
        verbose_name_plural = ArchiveConstants.VERBOSE_NAME_PLURAL
        ordering = ["position", "name"]

    objects = models.Manager()
    objects_in_site = InSiteManager()

    def __str__(self):
        return f"{self.name} <{self.slug}>"


class Collection(TimeBase, CategorizationBase):
    archive = models.ForeignKey(
        Archive,
        verbose_name=CollectionConstants.FIELD_ARCHIVE,
        help_text=CollectionConstants.FIELD_ARCHIVE_HELP_TEXT,
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
    is_visible = models.BooleanField(
        verbose_name=CollectionConstants.FIELD_IS_VISIBLE,
        help_text=CollectionConstants.FIELD_IS_VISIBLE_HELP_TEXT,
        default=True,
    )
    is_restricted = models.BooleanField(
        verbose_name=CollectionConstants.FIELD_IS_RESTRICTED,
        help_text=CollectionConstants.FIELD_IS_RESTRICTED_HELP_TEXT,
        default=False,
    )
    image = models.ImageField(
        verbose_name=CollectionConstants.FIELD_IMAGE,
        help_text=CollectionConstants.FIELD_IMAGE_HELP_TEXT,
        upload_to="collection_images",
        null=True,
    )

    class Meta:
        verbose_name = CollectionConstants.VERBOSE_NAME
        verbose_name_plural = CollectionConstants.VERBOSE_NAME_PLURAL
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
        verbose_name=CategoryConstants.FIELD_COLLECTION,
        help_text=CategoryConstants.FIELD_COLLECTION_HELP_TEXT,
        on_delete=models.SET_NULL,
        related_name="categories",
        null=True,
    )

    class Meta:
        verbose_name = CategoryConstants.VERBOSE_NAME
        verbose_name_plural = CategoryConstants.VERBOSE_NAME_PLURAL
        ordering = ["position", "slug"]
        unique_together = ["slug", "site"]

    objects = models.Manager()
    objects_in_site = InSiteManager()

    def __str__(self):
        return self.name

    @property
    def collection_slug(self):
        return self.collection.slug if self.collection_id else None

    @property
    def archive_slug(self):
        return (
            self.collection.archive.slug
            if self.collection_id and self.collection.archive_id
            else None
        )


class Person(TimeBase, CategorizationBase):
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="persons",
        default=settings.SITE_ID,
    )

    class Meta:
        verbose_name = PersonConstants.VERBOSE_NAME
        verbose_name_plural = PersonConstants.VERBOSE_NAME_PLURAL
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
        verbose_name = KeywordConstants.VERBOSE_NAME
        verbose_name_plural = KeywordConstants.VERBOSE_NAME_PLURAL
        ordering = ["position", "slug"]
        unique_together = ["slug", "site"]

    objects = models.Manager()
    objects_in_site = InSiteManager()

    def __str__(self):
        return self.name


class Piece(TimeBase):
    code = models.SlugField(
        verbose_name=PieceConstants.FIELD_CODE,
        help_text=PieceConstants.FIELD_CODE_HELP_TEXT,
        null=False,
        blank=False,
    )
    title = models.CharField(
        verbose_name=PieceConstants.FIELD_TITLE,
        help_text=PieceConstants.FIELD_TITLE_HELP_TEXT,
        max_length=512,
        null=False,
        blank=False,
    )
    thumb = models.ImageField(
        verbose_name=PieceConstants.FIELD_THUMB,
        help_text=PieceConstants.FIELD_THUMB_HELP_TEXT,
        upload_to="piece_thumbs",
        null=True,
        blank=True,
    )
    is_published = models.BooleanField(
        verbose_name=PieceConstants.FIELD_IS_PUBLISHED,
        help_text=PieceConstants.FIELD_IS_PUBLISHED_HELP_TEXT,
        default=False,
    )
    kind = models.CharField(
        verbose_name=PieceConstants.FIELD_KIND,
        help_text=PieceConstants.FIELD_KIND_HELP_TEXT,
        choices=PieceConstants.KIND_CHOICES,
        max_length=50,
        null=False,
        blank=False,
    )
    collection = models.ForeignKey(
        Collection,
        verbose_name=PieceConstants.FIELD_COLLECTION,
        help_text=PieceConstants.FIELD_COLLECTION_HELP_TEXT,
        on_delete=models.CASCADE,
        related_name="pieces",
        null=False,
    )
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name="pieces", default=settings.SITE_ID
    )
    categories = models.ManyToManyField(
        "Category",
        related_name="pieces",
        verbose_name=PieceConstants.FIELD_CATEGORIES,
        help_text=PieceConstants.FIELD_CATEGORIES_HELP_TEXT,
    )
    people = models.ManyToManyField(
        "Person",
        related_name="pieces",
        verbose_name=PieceConstants.FIELD_PEOPLE,
        help_text=PieceConstants.FIELD_PEOPLE_HELP_TEXT,
    )
    keywords = models.ManyToManyField(
        "Keyword",
        related_name="pieces",
        verbose_name=PieceConstants.FIELD_KEYWORDS,
        help_text=PieceConstants.FIELD_KEYWORDS_HELP_TEXT,
    )
    is_restricted = models.BooleanField(
        verbose_name=PieceConstants.FIELD_IS_RESTRICTED,
        help_text=PieceConstants.FIELD_IS_RESTRICTED_HELP_TEXT,
        default=False,
    )

    class Meta:
        verbose_name = PieceConstants.VERBOSE_NAME
        verbose_name_plural = PieceConstants.VERBOSE_NAME_PLURAL
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

    @property
    def thumb_url(self):
        thumb_url = self.thumb.url if self.thumb else None
        if thumb_url or self.kind != PieceConstants.KIND_VIDEO:
            return thumb_url
        active_provider = self.active_provider
        if (
            active_provider
            and active_provider.plyr_provider == ProviderConstants.YOUTUBE
        ):
            return ProviderConstants.THUMB_YOUTUBE_TEMPLATE.format(
                code=active_provider.ply_embed_id
            )


class Sequence(TimeBase):
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name="sequences")
    title = models.CharField(
        verbose_name=SequenceConstants.FIELD_TITLE,
        help_text=SequenceConstants.FIELD_TITLE_HELP_TEXT,
        max_length=500,
        null=True,
        blank=True,
    )
    content = models.TextField(
        verbose_name=SequenceConstants.FIELD_CONTENT,
        help_text=SequenceConstants.FIELD_CONTENT_HELP_TEXT,
        null=True,
        blank=True,
    )
    ini = models.TimeField(
        verbose_name=SequenceConstants.FIELD_INI,
        help_text=SequenceConstants.FIELD_INI_HELP_TEXT,
        null=False,
        blank=False,
    )
    end = models.TimeField(
        verbose_name=SequenceConstants.FIELD_END,
        help_text=SequenceConstants.FIELD_END_HELP_TEXT,
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = SequenceConstants.VERBOSE_NAME
        verbose_name_plural = SequenceConstants.VERBOSE_NAME_PLURAL
        ordering = ["ini"]

    objects = SequenceManager()

    @property
    def ini_sec(self):
        return self._time_to_seconds(self.ini)

    @property
    def end_sec(self):
        return self._time_to_seconds(self.end)

    def _time_to_seconds(self, time):
        return (time.hour * 60 + time.minute) * 60 + time.second

    def __str__(self):
        return f"Sequence <{self.id}>"


class Provider(models.Model):
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name="providers")
    active = models.BooleanField(
        verbose_name=ProviderConstants.FIELD_ACTIVE,
        help_text=ProviderConstants.FIELD_ACTIVE_HELP_TEXT,
        default=False,
    )
    ply_embed_id = models.CharField(
        verbose_name=ProviderConstants.FIELD_PLY_EMBED_ID,
        help_text=ProviderConstants.FIELD_PLY_EMBED_ID_HELP_TEXT,
        max_length=500,
        null=False,
        blank=False,
    )
    plyr_provider = models.CharField(
        verbose_name=ProviderConstants.FIELD_PLYR_PROVIDER,
        help_text=ProviderConstants.FIELD_PLYR_PROVIDER_HELP_TEXT,
        choices=ProviderConstants.PLYR_PROVIDER_CHOICES,
        max_length=50,
        null=False,
        blank=False,
    )
    image = models.ImageField(
        verbose_name=ProviderConstants.FIELD_IMAGE,
        help_text=ProviderConstants.FIELD_IMAGE_HELP_TEXT,
        upload_to="piece_images",
        null=True,
    )
    file = models.FileField(
        verbose_name=ProviderConstants.FIELD_FILE,
        help_text=ProviderConstants.FIELD_FILE_HELP_TEXT,
        upload_to="piece_files",
        null=True,
    )

    # to implement:
    online = models.BooleanField(
        verbose_name=ProviderConstants.FIELD_ONLINE, default=False
    )
    checked_at = models.DateTimeField(
        verbose_name=ProviderConstants.FIELD_CHECKED_AT, null=True, blank=True
    )

    class Meta:
        verbose_name = ProviderConstants.VERBOSE_NAME
        verbose_name_plural = ProviderConstants.VERBOSE_NAME_PLURAL
        ordering = ["active"]

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
        verbose_name=PieceMetaConstants.FIELD_EVENT,
        help_text=PieceMetaConstants.FIELD_EVENT_HELP_TEXT,
        max_length=500,
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name=PieceMetaConstants.FIELD_DESCRIPTION,
        help_text=PieceMetaConstants.FIELD_DESCRIPTION_HELP_TEXT,
        null=True,
        blank=True,
    )
    description_date = models.DateField(
        verbose_name=PieceMetaConstants.FIELD_DESCRIPTION_DATE,
        help_text=PieceMetaConstants.FIELD_DESCRIPTION_DATE_HELP_TEXT,
        null=True,
        blank=True,
    )
    location = models.CharField(
        verbose_name=PieceMetaConstants.FIELD_LOCATION,
        help_text=PieceMetaConstants.FIELD_LOCATION_HELP_TEXT,
        max_length=500,
        null=True,
        blank=True,
    )
    duration = models.TimeField(
        verbose_name=PieceMetaConstants.FIELD_DURATION,
        help_text=PieceMetaConstants.FIELD_DURATION_HELP_TEXT,
        null=True,
        blank=True,
    )
    register_date = models.DateField(
        verbose_name=PieceMetaConstants.FIELD_REGISTER_DATE,
        help_text=PieceMetaConstants.FIELD_REGISTER_DATE_HELP_TEXT,
        null=True,
        blank=True,
    )
    register_author = models.CharField(
        verbose_name=PieceMetaConstants.FIELD_REGISTER_AUTHOR,
        help_text=PieceMetaConstants.FIELD_REGISTER_AUTHOR_HELP_TEXT,
        max_length=500,
        null=True,
        blank=True,
    )
    productor = models.CharField(
        verbose_name=PieceMetaConstants.FIELD_PRODUCTOR,
        help_text=PieceMetaConstants.FIELD_PRODUCTOR_HELP_TEXT,
        max_length=500,
        null=True,
        blank=True,
    )
    notes = models.TextField(
        verbose_name=PieceMetaConstants.FIELD_NOTES,
        help_text=PieceMetaConstants.FIELD_NOTES_HELP_TEXT,
        null=True,
        blank=True,
    )
    archivist_notes = models.TextField(
        verbose_name=PieceMetaConstants.FIELD_ARCHIVIST_NOTES,
        help_text=PieceMetaConstants.FIELD_ARCHIVIST_NOTES_HELP_TEXT,
        null=True,
        blank=True,
    )
    documentary_unit = models.CharField(
        verbose_name=PieceMetaConstants.FIELD_DOCUMENTARY_UNIT,
        help_text=PieceMetaConstants.FIELD_DOCUMENTARY_UNIT_HELP_TEXT,
        max_length=500,
        null=True,
        blank=True,
    )
    lang = models.CharField(
        verbose_name=PieceMetaConstants.FIELD_LANG,
        help_text=PieceMetaConstants.FIELD_LANG_HELP_TEXT,
        max_length=500,
        null=True,
        blank=True,
    )
    original_format = models.CharField(
        verbose_name=PieceMetaConstants.FIELD_ORIGINAL_FORMAT,
        help_text=PieceMetaConstants.FIELD_ORIGINAL_FORMAT_HELP_TEXT,
        max_length=500,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = PieceMetaConstants.VERBOSE_NAME
        verbose_name_plural = PieceMetaConstants.VERBOSE_NAME_PLURAL

    def __str__(self):
        return f"PieceMeta <of {self.piece_id}>"


class Place(TimeBase):
    name = models.CharField(
        verbose_name=PlaceConstants.FIELD_NAME,
        help_text=PlaceConstants.FIELD_NAME_HELP_TEXT,
        max_length=500,
        null=False,
        blank=False,
    )
    allowed_pieces = models.ManyToManyField(
        Piece,
        related_name="allowed_places",
        verbose_name=PlaceConstants.FIELD_ALLOWED_PIECES,
        help_text=PlaceConstants.FIELD_ALLOWED_PIECES_HELP_TEXT,
    )
    allowed_collections = models.ManyToManyField(
        Collection,
        related_name="allowed_places",
        verbose_name=PlaceConstants.FIELD_ALLOWED_COLLECTIONS,
        help_text=PlaceConstants.FIELD_ALLOWED_COLLECTIONS_HELP_TEXT,
    )
    allowed_archives = models.ManyToManyField(
        Archive,
        related_name="allowed_places",
        verbose_name=PlaceConstants.FIELD_ALLOWED_ARCHIVES,
        help_text=PlaceConstants.FIELD_ALLOWED_ARCHIVES_HELP_TEXT,
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
        verbose_name = PlaceConstants.VERBOSE_NAME
        verbose_name_plural = PlaceConstants.VERBOSE_NAME_PLURAL
        ordering = ["name"]

    def __str__(self):
        return f"Place <{self.name}>"


class PlaceAddress(TimeBase):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="addresses")
    ipv4 = models.GenericIPAddressField(
        verbose_name=PlaceAddressConstants.FIELD_IPV4,
        help_text=PlaceAddressConstants.FIELD_IPV4_HELP_TEXT,
        unique=True,
        null=False,
        blank=False,
        db_index=True,
    )
    description = models.CharField(
        verbose_name=PlaceAddressConstants.FIELD_DESCRIPTION,
        help_text=PlaceAddressConstants.FIELD_DESCRIPTION_HELP_TEXT,
        max_length=500,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = PlaceAddressConstants.VERBOSE_NAME
        verbose_name_plural = PlaceAddressConstants.VERBOSE_NAME_PLURAL
        ordering = ["ipv4"]

    def __str__(self):
        return f"PlaceAddress <{self.ipv4}>"
