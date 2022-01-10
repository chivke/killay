from django import forms

from killay.pages.lib.constants import PageConstants
from killay.pages.models import Page
from killay.admin.utils import ImageFileInput


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = [
            "title",
            "slug",
            "kind",
            "is_visible",
            "is_visible_in_navbar",
            "is_visible_in_footer",
            "is_title_visible_in_body",
            "position",
            "redirect_to",
            "header_image",
            "body",
            "collection_site",
        ]

    kind = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "ui fluid dropdown"}),
        required=True,
        choices=PageConstants.KIND_CHOICES,
    )
    header_image = forms.ImageField(widget=ImageFileInput(), required=False)
