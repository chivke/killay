from django import forms

from cmpirque.admin.models import AdminConfiguration, SocialMedia


class AdminConfigurationForm(forms.ModelForm):
    class Meta:
        model = AdminConfiguration
        fields = ["site_name", "is_published"]


class SocialMediaForm(forms.ModelForm):
    class Meta:
        model = SocialMedia
        fields = ["provider", "url", "css_class", "is_visible"]


SocialMediaFormSet = forms.inlineformset_factory(
    AdminConfiguration, SocialMedia, form=SocialMediaForm, extra=1
)
