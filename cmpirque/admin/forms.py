from django import forms

from cmpirque.admin.models import SiteConfiguration, SocialMedia


class SiteConfigurationForm(forms.ModelForm):
    class Meta:
        model = SiteConfiguration
        fields = ["name", "domain", "is_published"]


class SocialMediaForm(forms.ModelForm):
    class Meta:
        model = SocialMedia
        fields = ["provider", "url", "css_class", "is_visible"]


SocialMediaFormSet = forms.inlineformset_factory(
    SiteConfiguration, SocialMedia, form=SocialMediaForm, extra=1
)
