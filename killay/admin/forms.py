from django import forms

from killay.admin.models import Logo, SiteConfiguration, SocialMedia
from killay.admin.utils import ImageFileInput
from killay.archives.models import Archive, Category, Collection


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


class ArchiveForm(forms.ModelForm):
    class Meta:
        model = Archive
        fields = ["name", "slug", "description", "position"]

    description = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"rows": 1})
    )


ArchiveFormSet = forms.modelformset_factory(
    Archive, form=ArchiveForm, extra=1, can_delete=True
)


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ["name", "slug", "description", "position", "archive"]

    description = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"rows": 1})
    )


CollectionFormSet = forms.modelformset_factory(
    Collection, form=CollectionForm, extra=1, can_delete=True
)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug", "description", "position"]

    description = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"rows": 1})
    )


CategoryFormSet = forms.modelformset_factory(
    Category, form=CategoryForm, extra=1, can_delete=True
)
