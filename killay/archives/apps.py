from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ArchivesConfig(AppConfig):
    name = "killay.archives"
    verbose_name = _("Archives")
    default_auto_field = "django.db.models.BigAutoField"
