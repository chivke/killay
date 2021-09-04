from django.forms import ClearableFileInput


class ImageFileInput(ClearableFileInput):
    template_name = "admin/components/field_image_input.html"
