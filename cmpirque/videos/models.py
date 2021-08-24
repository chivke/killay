import requests

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone

from cmpirque.videos.lib.constants import VideoProviderConstants


class Video(models.Model):
    code = models.SlugField(null=False, blank=False, unique=True, db_index=True)
    is_visible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumb = models.ImageField(null=True, blank=True)
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


class VideoMeta(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    description_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=500, null=True, blank=True)
    duration = models.TimeField(null=True, blank=True)
    register_date = models.DateField(null=True, blank=True)
    register_author = models.CharField(max_length=500, null=True, blank=True)
    productor = models.CharField(max_length=500, null=True, blank=True)
    status = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

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
        other_providers = self.get_related_providers()
        if self.active and other_providers.exists():
            other_providers.update(active=False)
        if not self.online or not self.checked_at:
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

    def get_related_providers(self):
        return VideoProvider.objects.filter(video_id=self.video_id).exclude(id=self.id)


class VideoSequenceManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by("ini")

    def get_ordered_data(self, *args):
        sequences = self.values(*args)
        return [
            {**sequence, "order": index + 1} for index, sequence in enumerate(sequences)
        ]


class VideoSequence(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="sequences")
    title = models.CharField(max_length=500, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    ini = models.PositiveSmallIntegerField(null=False, blank=False)
    end = models.PositiveSmallIntegerField(null=False, blank=False)

    class Meta:
        verbose_name = "video sequence"
        verbose_name_plural = "video sequences"

    objects = VideoSequenceManager()

    def clean(self):
        super().clean()
        self.validate_ini_greater_then_end()

    def validate_ini_greater_then_end(self):
        if (
            isinstance(self.ini, int)
            and isinstance(self.end, int)
            and self.ini >= self.end
        ):
            raise ValidationError("init of sequence must be greater then end")


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
    slug = models.SlugField(null=False, blank=False, unique=True, db_index=True)
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
    slug = models.SlugField(null=False, blank=False, unique=True, db_index=True)
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
    slug = models.SlugField(null=False, blank=False, unique=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "keyword"
        verbose_name_plural = "keywords"
        ordering = ["position"]

    def __str__(self):
        return self.name
