import requests
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy

from cmpirque.admin.utils import InSiteManager
from cmpirque.videos.lib.constants import VideoProviderConstants
from cmpirque.videos.utils import parse_sequences_from_vtt_file


class Video(models.Model):
    code = models.SlugField(
        gettext_lazy("Code"), null=False, blank=False, unique=True, db_index=True
    )
    is_visible = models.BooleanField(gettext_lazy("Is visible"), default=False)
    created_at = models.DateTimeField(gettext_lazy("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(gettext_lazy("Updated at"), auto_now=True)
    thumb = models.ImageField(
        gettext_lazy("Thumb"), upload_to="video_thumbs", null=True, blank=True
    )
    meta = models.OneToOneField(
        "VideoMeta", on_delete=models.CASCADE, related_name="video"
    )
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name="videos", default=settings.SITE_ID
    )

    class Meta:
        verbose_name = gettext_lazy("video")
        verbose_name_plural = gettext_lazy("videos")
        ordering = ["code"]

    objects = InSiteManager()

    def __str__(self):
        return f"Video <{self.code}>"

    def get_absolute_url(self):
        return reverse("videos:detail", kwargs={"slug": self.code})

    @property
    def active_provider(self):
        return self.providers.filter(active=True).first()

    @property
    def has_sequences(self):
        return self.sequences.exists()

    def import_from_vtt_file(self, path):
        data_for_import = parse_sequences_from_vtt_file(path)
        with transaction.atomic():
            sequences = self.sequences.bulk_create(
                [VideoSequence(video_id=self.id, **data) for data in data_for_import]
            )
        return sequences


class VideoMeta(models.Model):
    title = models.CharField(gettext_lazy("Title"), max_length=500)
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
        verbose_name = gettext_lazy("video metadata")
        verbose_name_plural = gettext_lazy("video metadatas")


class VideoProvider(models.Model):
    active = models.BooleanField(gettext_lazy("Active"), default=False)
    online = models.BooleanField(gettext_lazy("Online"), default=False)
    checked_at = models.DateTimeField(gettext_lazy("Checked at"), null=True, blank=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="providers")
    ply_embed_id = models.CharField(
        gettext_lazy("Ply Embed ID"), max_length=500, null=False, blank=False
    )
    plyr_provider = models.CharField(
        gettext_lazy("Ply Provider"),
        choices=VideoProviderConstants.PLYR_PROVIDER_CHOICES,
        max_length=50,
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = gettext_lazy("video provider")
        verbose_name_plural = gettext_lazy("video provider")

    def save(self, *args, **kwargs):
        if self.pk:
            current_video = self.__class__.objects.get(id=self.id)

        other_providers = self.get_related_providers()
        if self.active and other_providers.exists():
            other_providers.update(active=False)
        if (
            not self.online
            or not self.checked_at
            or current_video.ply_embed_id != self.ply_embed_id
            or current_video.plyr_provider != self.plyr_provider
        ):
            self.check_is_online()
        super().save(*args, **kwargs)

    def check_is_online(self):
        try:
            response = requests.get(self.video_url)
        except requests.ConnectionError:
            self.online = False
        else:
            self.online = self.ply_embed_id in str(response.content)
        self.checked_at = timezone.now()
        return self.online

    @property
    def video_url(self):
        if self.plyr_provider == VideoProviderConstants.VIMEO:
            return f"https://player.{self.plyr_provider}.com/video/{self.ply_embed_id}"
        else:
            return f"https://www.{self.plyr_provider}.com/embed/{self.ply_embed_id}"

    @property
    def video_url_for_plyr(self):
        if self.plyr_provider == VideoProviderConstants.VIMEO:
            return self.video_url + (
                "?loop=false&amp;byline=false&amp;portrait=false"
                "&amp;title=false&amp;speed=true&amp;transparent=0&amp;gesture=media"
            )
        else:
            return self.video_url + (
                "?origin=https://plyr.io&amp;iv_load_policy=3&amp;modestbranding=1&amp;responsive=true"
                "&amp;playsinline=1&amp;showinfo=0&amp;rel=0&amp;enablejsapi=1"
            )

    def get_related_providers(self):
        return VideoProvider.objects.filter(video_id=self.video_id).exclude(id=self.id)


class VideoSequenceManager(models.Manager):
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


class VideoSequence(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="sequences")
    title = models.CharField(
        gettext_lazy("Title"), max_length=500, null=True, blank=True
    )
    content = models.TextField(gettext_lazy("Content"), null=True, blank=True)
    ini = models.TimeField(gettext_lazy("Initiation"), null=False, blank=False)
    end = models.TimeField(gettext_lazy("End"), null=False, blank=False)

    class Meta:
        verbose_name = gettext_lazy("video sequence")
        verbose_name_plural = gettext_lazy("video sequences")
        ordering = ["ini"]

    objects = VideoSequenceManager()

    def clean(self):
        super().clean()
        self.validate_ini_greater_then_end()

    def validate_ini_greater_then_end(self):
        if self.ini and self.end and self.ini >= self.end:
            raise ValidationError("init of sequence must be greater then end")

    @property
    def ini_sec(self):
        return self.__time_to_seconds(self.ini)

    @property
    def end_sec(self):
        return self.__time_to_seconds(self.end)

    def __time_to_seconds(self, time):
        return (time.hour * 60 + time.minute) * 60 + time.second


class VideoCategorization(models.Model):
    video = models.OneToOneField(
        Video, on_delete=models.CASCADE, related_name="categorization"
    )
    categories = models.ManyToManyField(
        "VideoCategory", related_name="videos", verbose_name="Categories"
    )
    people = models.ManyToManyField(
        "VideoPerson", related_name="videos", verbose_name="People"
    )
    keywords = models.ManyToManyField(
        "VideoKeyword", related_name="videos", verbose_name="Keywords"
    )

    class Meta:
        verbose_name = gettext_lazy("video categorization")
        verbose_name_plural = gettext_lazy("video categorizations")


class VideoFilterAbstract(models.Model):
    name = models.CharField(
        gettext_lazy("Name"), max_length=255, null=False, blank=False
    )
    slug = models.SlugField(
        gettext_lazy("Slug"), max_length=255, null=False, blank=False, db_index=True
    )
    description = models.TextField(gettext_lazy("Description"), null=True, blank=True)
    position = models.PositiveSmallIntegerField(gettext_lazy("Position"), default=0)
    # site = models.ForeignKey(
    #     Site, on_delete=models.CASCADE, related_name="pages", default=settings.SITE_ID
    # )

    class Meta:
        abstract = True

    objects = InSiteManager()

    def __str__(self):
        return f"{self.name} <{self.slug}>"


class VideoCategory(VideoFilterAbstract):
    # name = models.CharField(
    #     gettext_lazy("Name"), max_length=255, null=False, blank=False
    # )
    # slug = models.SlugField(
    #     gettext_lazy("Slug"),
    #     max_length=255,
    #     null=False,
    #     blank=False,
    #     db_index=True,
    # )
    # description = models.TextField(gettext_lazy("Description"), null=True, blank=True)
    # position = models.PositiveSmallIntegerField(gettext_lazy("Position"), default=0)
    # site = models.ForeignKey(
    #     Site, on_delete=models.CASCADE, related_name="pages", default=settings.SITE_ID
    # )
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="video_categories",
        default=settings.SITE_ID,
    )

    class Meta:
        verbose_name = gettext_lazy("category")
        verbose_name_plural = gettext_lazy("categories")
        ordering = ["position", "slug"]
        unique_together = ["slug", "site"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("videos:category-list", kwargs={"slug": self.slug})


class VideoPerson(VideoFilterAbstract):
    # name = models.CharField(
    #     gettext_lazy("Name"), max_length=255, null=False, blank=False
    # )
    # slug = models.SlugField(
    #     gettext_lazy("Slug"),
    #     max_length=255,
    #     null=False,
    #     blank=False,
    #     unique=True,
    #     db_index=True,
    # )
    # description = models.TextField(gettext_lazy("Description"), null=True, blank=True)
    # position = models.PositiveSmallIntegerField(gettext_lazy("Position"), default=0)
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="video_people",
        default=settings.SITE_ID,
    )

    class Meta:
        verbose_name = gettext_lazy("person")
        verbose_name_plural = gettext_lazy("people")
        ordering = ["position", "slug"]
        unique_together = ["slug", "site"]

    def __str__(self):
        return self.name


class VideoKeyword(VideoFilterAbstract):
    # name = models.CharField(
    #     gettext_lazy("Name"), max_length=255, null=False, blank=False
    # )
    # slug = models.SlugField(
    #     gettext_lazy("Slug"),
    #     max_length=255,
    #     null=False,
    #     blank=False,
    #     unique=True,
    #     db_index=True,
    # )
    # description = models.TextField(gettext_lazy("Description"), null=True, blank=True)
    # position = models.PositiveSmallIntegerField(gettext_lazy("Position"), default=0)
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="video_keywords",
        default=settings.SITE_ID,
    )

    class Meta:
        verbose_name = gettext_lazy("keyword")
        verbose_name_plural = gettext_lazy("keywords")
        ordering = ["position", "slug"]
        unique_together = ["slug", "site"]

    def __str__(self):
        return self.name
