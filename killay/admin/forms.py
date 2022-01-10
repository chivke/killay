from django import forms

from killay.admin.models import Logo, SiteConfiguration, SocialMedia
from killay.admin.utils import ImageFileInput


class SiteConfigurationForm(forms.ModelForm):
    class Meta:
        model = SiteConfiguration
        fields = [
            "name",
            "domain",
            "is_published",
            "footer_is_visible",
            "collection_site",
        ]


class SocialMediaForm(forms.ModelForm):
    class Meta:
        model = SocialMedia
        fields = ["provider", "url", "is_visible", "position"]


SocialMediaFormSet = forms.inlineformset_factory(
    SiteConfiguration, SocialMedia, form=SocialMediaForm, extra=1
)


class LogoForm(forms.ModelForm):
    class Meta:
        model = Logo
        fields = ["name", "image", "is_visible", "position"]

    image = forms.ImageField(widget=ImageFileInput())


LogoFormSet = forms.inlineformset_factory(
    SiteConfiguration, Logo, form=LogoForm, extra=1
)
