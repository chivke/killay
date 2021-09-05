from django.conf import settings
from django.db.models import Manager
from django.forms import ClearableFileInput, Textarea


class ImageFileInput(ClearableFileInput):
    template_name = "admin/components/field_image_input.html"


class QuillTextarea(Textarea):
    template_name = "admin/components/field_html_input.html"
    form_id = "generic_form_id"

    def get_context(self, name, value, attrs):
        return {
            "widget": {
                "name": name,
                "is_hidden": self.is_hidden,
                "required": self.is_required,
                "value": self.format_value(value),
                "attrs": self.build_attrs(self.attrs, attrs),
                "template_name": self.template_name,
                "form_id": self.form_id,
            }
        }


class InSiteManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(site_id=settings.SITE_ID)
