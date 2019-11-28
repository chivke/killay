# -*- coding: utf-8 -*-
from django.db import models
# django category:
#from category.models import Category
#from category.models import Tag
# djangoCMS integration:
from cms.models.fields import PlaceholderField
from cms.models import CMSPlugin
#from cms.extensions import PageExtension
#from cms.extensions.extension_pool import extension_pool
# utils:
import time
#from model_utils.models import TimeStampedModel
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings

from django.template.defaultfilters import truncatechars

# ..
# Main Models for VideoLog
# -------------------------
# ..

class VideoCategory(models.Model):
    """
    Represents a video categories.| Representa categorías de video
    """
    title = models.CharField(
        max_length=255,
        help_text="short descriptive name for this category. | nombre descriptivo corto para esta categoría",
    )
    subtitle = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        default="",
        help_text="subtitule for this category | subtítulo para esta categoría",
    )
    slug = models.SlugField(
        max_length=255,
        db_index=True,
        unique=True,
        help_text="Short descriptive unique name for use in urls | nombre corto, descriptivo y único para usar en urls",
    )
    #parent = models.ForeignKey(
    #    "self", null=True, blank=True, on_delete=models.CASCADE
    #)
    sites = models.ManyToManyField(
        "sites.Site",
        blank=True,
        help_text="Limits category scope to selected sites. | Limitar categoría al alcance de sitios seleccionados",
    )
    header_image = FilerFileField(
        help_text="Page header image/ imagen de cabecera para página ",
        related_name="header_image_videocategory",
        blank=True,
        null=True,
        )
    subheader_image = FilerFileField(
        help_text="Page subheader image/ imagen de subcabecera para página ",
        related_name="subheader_image_videocategory",
        blank=True,
        null=True,
        )

    def __unicode__(self):
        if self.subtitle:
            return "%s - %s" % (self.title, self.subtitle)
        else:
            return self.title

    __str__ = __unicode__

    class Meta:
        ordering = ("title",)
        verbose_name = "video category | categoría de video"
        verbose_name_plural = "videos categories | categorías de video"

    #def save(self, *args, **kwargs):
    #    # Raise on circular reference
    #    parent = self.parent
    #    while parent is not None:
    #        if parent == self:
    #            raise RuntimeError("Circular references not allowed")
    #        parent = parent.parent

    #    super(VideoCategory, self).save(*args, **kwargs)

    #@property
    #def children(self):
    #    return self.videocategory_set.all().order_by("title")

    #@property
    #def people(self):
    #    return VideoPeople.objects.filter(categories__in=[self]).order_by("title")
    #@property
    #def keywords(self):
    #    return VideoKeywords.objects.filter(categories__in=[self]).order_by("title")

    def get_absolute_url(self):
        return reverse("videolog:catentries", args=[self.slug])

class VideoPeople(models.Model):
    """
    Represents a video people tag | Representa etiquetas de personas, comunidades y pueblos.
    """
    title = models.CharField(
        max_length=200,
        help_text="Short descriptive name for this video people tag. | nombre descriptivo corto para esta etiqueta de personas.",
    )
    slug = models.SlugField(
        max_length=255,
        db_index=True,
        unique=True,
        help_text="Short descriptive unique name for use in urls. | nombre corto, descriptivo y único para usar en urls",
    )
    # categories = models.ManyToManyField(
    #     "VideoCategory",
    #     blank=True,
    #     help_text="Categories to which this video people tag belongs. | Categorías en donde aplica etiqueta de personas."
    # )
    header_image = FilerFileField(
        help_text="Page header image/ imagen de cabecera para página ",
        related_name="header_image_videopeople",
        blank=True,
        null=True,
        )
    subheader_image = FilerFileField(
        help_text="Page subheader image/ imagen de subcabecera para página ",
        related_name="subheader_image_videopeople",
        blank=True,
        null=True,
        )

    def __unicode__(self):
        return self.title

    __str__ = __unicode__

    class Meta:
        ordering = ("title",)
        verbose_name = "video people tag | etiqueta de personas en videos"
        verbose_name_plural = "video people tags | etiquetas de personas en videos"

    def get_absolute_url(self):
        return reverse("videolog:popentries", args=[self.slug])

class VideoKeywords(models.Model):
    """
    Represents a video keywords | Representa palabras clave de personas, comunidades y pueblos.
    """
    title = models.CharField(
        max_length=200,
        help_text="Short descriptive name for this video keywords. | nombre descriptivo corto para esta keyword de video",
    )
    slug = models.SlugField(
        max_length=255,
        db_index=True,
        unique=True,
        help_text="Short descriptive unique name for use in urls. | nombre corto, descriptivo y único para usar en urls",
    )
    # categories = models.ManyToManyField(
    #     "VideoCategory",
    #     blank=True,
    #     help_text="Categories to which this video keyword belongs. | Categorías en donde pertenece esta palabra clave de video"
    # )
    header_image = FilerFileField(
        help_text="Page header image/ imagen de cabecera para página ",
        related_name="header_image_videokeywords",
        blank=True,
        null=True,
        )
    subheader_image = FilerFileField(
        help_text="Page subheader image/ imagen de subcabecera para página ",
        related_name="subheader_image_videokeywords",
        blank=True,
        null=True,
        )

    def __unicode__(self):
        return self.title

    __str__ = __unicode__

    class Meta:
        ordering = ("title",)
        verbose_name = "video keyword | palabra clave para videos"
        verbose_name_plural = "video keywords | palabras clave para videos"

    def get_absolute_url(self):
        return reverse("videolog:keyentries", args=[self.slug])

class VideoEntry(models.Model):
    """
    Represents a video entry.| Representa una entrada de video.
    Fields to catalogizer the video entries. |
    Campos para catalogar las entradas de video.
    """
    # metadata of video:
    title = models.CharField(max_length=255,
        help_text="title for video/ título del video",
        )
    video_code = models.CharField(max_length=10,
        help_text="code for video / código del video",
        #db_index=True,
        #unique=True,
        #editable=False,
        )
    category = models.ManyToManyField('VideoCategory', 
        help_text="video category / categoría del video",
        #null=True, 
        blank=True,
        #editable=True,
        #on_delete=models.CASCADE
        )
    register_date = models.DateField(default='1990-01-01',
        help_text="date of video register / fecha de registro",
        null=True,
        blank=True,
        )
    people = models.ManyToManyField('VideoPeople',
        help_text="communities & people / comunidades, personas y pueblos",
        #null=True,
        blank=True,
        )
    location = models.CharField(max_length=255,
        help_text="location of video / lugar del video",
        null=True,
        blank=True,
        )
    duration = models.TimeField(default='00:00:00',
        help_text="duration of video / duración del video",
        null=True,
        blank=True,
        )
    productor = models.CharField(max_length=255,
        help_text="corporate productor / productor corporativo",
        null=True,
        blank=True,
        )
    register_author = models.CharField(max_length=255,
        help_text="register author / autor del registro",
        null=True,
        blank=True,
        )
    keywords = models.ManyToManyField('VideoKeywords',
        help_text="keywords / palabras clave",
        #null=True,
        blank=True,
        )
    description = models.TextField(max_length=700,
        help_text="description / descripción",
        null=True,
        blank=True,
        )
    status = models.CharField(max_length=255,
        help_text="status / estado",
        null=True,
        blank=True,
        )
    notes = models.CharField(max_length=255,
        help_text="notes / notas",
        null=True,
        blank=True,
        )
    desc_date = models.DateField(default='2000-01-01',
        help_text="date of description / fecha de descripción",
        null=True,
        blank=True,
        )
    # video media fields:
    video_file = models.FileField(
        help_text="video file / archivo de video",
        #related_name="file_video_videoentry",
        null=True,
        blank=True,
        )
    video_thumb = models.FileField(
        help_text="video thumb / imagen de video",
        #related_name="file_thumb_videoentry",
        null=True,
        blank=True,
        )
    track_chapters = models.FileField(
        help_text="chapters track / archivo de capítulos",
        #related_name="track_chapters_videoentry",
        null=True,
        blank=True,
        )
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    #description = models.TextField(default="Una descripción",max_length=600)
    #video_date = models.DateField(default='1990-01-01')
    #video_placeholder = PlaceholderField('video',related_name='video')
    # django-category:
    #category = models.ForeignKey(Category, editable=True, on_delete=models.CASCADE)
    #category = models.ForeignKey('VideoCategory', null=True, blank=True)
    #tags = models.ManyToManyField('category.Tag', help_text='Etiqueta este item')
    # meta_cms_data
    is_published = models.BooleanField(default=False)
    published_timestamp = models.DateTimeField(blank=True, null=True, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, editable=True, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "video entry/ entrada de video"
        verbose_name_plural = "video entries / entradas de video"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('videolog:entrydetail', args=[self.slug])

    def _insert_timestamp(self, slug, max_length=255):
        """Appends a timestamp integer to the given slug, yet ensuring the
        result is less than the specified max_length.
        """
        timestamp = str(int(time.time()))
        ts_len = len(timestamp) + 1
        while len(slug) + ts_len > max_length:
            slug = '-'.join(slug.split('-')[:-1])
        slug = '-'.join([slug, timestamp])
        return slug

    def _slugify_title(self):
        """Slugify the Entry title, but ensure it's less than the maximum
        number of characters. This method also ensures that a slug is unique by
        appending a timestamp to any duplicate slugs.
        """
        # Restrict slugs to their maximum number of chars, but don't split mid-word
        self.slug = slugify(self.title)
        while len(self.slug) > 255:
            self.slug = '-'.join(self.slug.split('-')[:-1])
        # Is the same slug as another entry?
        if VideoEntry.objects.filter(slug=self.slug).exclude(id=self.id).exists():
            # Append time to differentiate.
            self.slug = self._insert_timestamp(self.slug)
    def save(self, *args, **kwargs):
        self._slugify_title()
        # Time to publish?
        if not self.published_timestamp and self.is_published:
            self.published_timestamp = timezone.now()
        elif not self.is_published:
            self.published_timestamp = None
        super(VideoEntry, self).save(*args, **kwargs)
        
# ..
# djangoCMS Plugin Models for VideoLog
# ---------------------------------------
# ..
class VideoEntryPluginModel(CMSPlugin):
    entry = models.ForeignKey(VideoEntry)
    def __unicode__(self):
        return self.title
