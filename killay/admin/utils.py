from django.conf import settings
from django.db.models import Manager
from django.forms import ClearableFileInput


class ImageFileInput(ClearableFileInput):
    template_name = "admin/components/field_image_input.html"


class InSiteManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(site_id=settings.SITE_ID)
