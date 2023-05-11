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


class ArchiveListForm(forms.ModelForm):
    class Meta:
        model = Archive
        fields = ["name", "slug", "description", "position"]

    name = forms.CharField(disabled=True)
    slug = forms.CharField(disabled=True)
    description = forms.CharField(disabled=True)


ArchiveFormSet = forms.modelformset_factory(
    Archive, form=ArchiveListForm, extra=0, can_delete=False
)


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ["name", "slug", "description", "position", "archive"]

    description = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"rows": 1})
    )


class CollectionListForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ["name", "slug", "position", "archive"]

    name = forms.CharField(disabled=True)
    slug = forms.CharField(disabled=True)


CollectionFormSet = forms.modelformset_factory(
    Collection, form=CollectionListForm, extra=0, can_delete=False
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
