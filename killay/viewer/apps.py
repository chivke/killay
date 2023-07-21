from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ViewerConfig(AppConfig):
    name = "killay.viewer"
    verbose_name = _("Viewer")
    default_auto_field = "django.db.models.BigAutoField"
