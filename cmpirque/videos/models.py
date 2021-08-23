from django.db import models
from django.urls import reverse

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

    def __str__(self):
        return f"Video <{self.code}>"

    def get_absolute_url(self):
        return reverse("videos:detail", kwargs={"slug": self.code})


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
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="providers")
    ply_embed_id = models.CharField(max_length=500, null=False, blank=False)
    plyr_provider = models.CharField(
        choices=VideoProviderConstants.PLYR_PROVIDER_CHOICES,
        max_length=50,
        null=False,
        blank=False,
    )


class VideoSequenceManager(models.Manager):
    def get_ordered_data(self, *args):
        sequences = self.order_by("ini").values(*args)
        return [
            {**sequence, "order": index + 1} for index, sequence in enumerate(sequences)
        ]


class VideoSequence(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="sequences")
    title = models.CharField(max_length=500, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    ini = models.PositiveSmallIntegerField(null=False)
    end = models.PositiveSmallIntegerField(null=False)

    class Meta:
        verbose_name = "video sequence"
        verbose_name_plural = "video sequences"

    objects = VideoSequenceManager()


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


class VideoPerson(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(null=False, blank=False, unique=True, db_index=True)
    description = models.TextField(null=True, blank=True)


class VideoKeyword(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(null=False, blank=False, unique=True, db_index=True)
    description = models.TextField(null=True, blank=True)
