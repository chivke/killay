import requests
from time import strptime
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy

from cmpirque.videos.lib.constants import VideoProviderConstants
from cmpirque.videos.utils import parse_sequences_from_vtt_file


class Video(models.Model):
    code = models.SlugField(null=False, blank=False, unique=True, db_index=True)
    is_visible = models.BooleanField(gettext_lazy("Is visible"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumb = models.ImageField(upload_to="video_thumbs", null=True, blank=True)
    meta = models.OneToOneField(
        "VideoMeta", on_delete=models.CASCADE, related_name="video"
    )

    class Meta:
        verbose_name = "video"
        verbose_name_plural = "videos"
        ordering = ["code"]

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
    title = models.CharField(max_length=500)
    event = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    description_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=500, null=True, blank=True)
    duration = models.TimeField(null=True, blank=True)
    register_date = models.DateField(null=True, blank=True)
    register_author = models.CharField(max_length=500, null=True, blank=True)
    productor = models.CharField(max_length=500, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    archivist_notes = models.TextField(null=True, blank=True)
    documentary_unit = models.CharField(max_length=500, null=True, blank=True)
    lang = models.CharField(max_length=500, null=True, blank=True)
    original_format = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = "video metadata"
        verbose_name_plural = "video metadatas"


class VideoProvider(models.Model):
    active = models.BooleanField(default=False)
    online = models.BooleanField(default=False)
    checked_at = models.DateTimeField(null=True, blank=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="providers")
    ply_embed_id = models.CharField(max_length=500, null=False, blank=False)
    plyr_provider = models.CharField(
        choices=VideoProviderConstants.PLYR_PROVIDER_CHOICES,
        max_length=50,
        null=False,
        blank=False,
    )

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
    def get_queryset(self):
        return super().get_queryset().order_by("ini")

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
    title = models.CharField(max_length=500, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    ini = models.TimeField(null=False, blank=False)
    end = models.TimeField(null=False, blank=False)

    class Meta:
        verbose_name = "video sequence"
        verbose_name_plural = "video sequences"

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
    categories = models.ManyToManyField("VideoCategory", related_name="videos")
    people = models.ManyToManyField("VideoPerson", related_name="videos")
    keywords = models.ManyToManyField("VideoKeyword", related_name="videos")

    class Meta:
        verbose_name = "video categorization"
        verbose_name_plural = "video categorizations"


class VideoCategory(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(
        max_length=255, null=False, blank=False, unique=True, db_index=True
    )
    description = models.TextField(null=True, blank=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ["position"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("videos:category-list", kwargs={"slug": self.slug})


class VideoPerson(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(
        max_length=255, null=False, blank=False, unique=True, db_index=True
    )
    description = models.TextField(null=True, blank=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "person"
        verbose_name_plural = "people"
        ordering = ["position"]

    def __str__(self):
        return self.name


class VideoKeyword(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(
        max_length=255, null=False, blank=False, unique=True, db_index=True
    )
    description = models.TextField(null=True, blank=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "keyword"
        verbose_name_plural = "keywords"
        ordering = ["position"]

    def __str__(self):
        return self.name
