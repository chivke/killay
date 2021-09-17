from django import forms

from killay.pages.models import Page
from killay.admin.utils import ImageFileInput


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = [
            "title",
            "slug",
            "is_visible",
            "is_visible_in_navbar",
            "is_visible_in_footer",
            "header_image",
            "body",
        ]

    header_image = forms.ImageField(widget=ImageFileInput(), required=False)
