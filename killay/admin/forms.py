from django import forms

from killay.admin.models import Logo, SiteConfiguration, SocialMedia
from killay.admin.utils import ImageFileInput
from killay.archives.lib.constants import PieceConstants
from killay.archives.models import (
    Archive,
    Category,
    Collection,
    Keyword,
    Person,
    Piece,
    PieceMeta,
)


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

    description = forms.CharField(required=False, widget=forms.Textarea())


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
        fields = ["archive", "name", "slug", "description", "position"]

    archive = forms.ModelChoiceField(
        queryset=Archive.objects_in_site.all(),
        widget=forms.Select(attrs={"class": "ui fluid dropdown"}),
        required=False,
    )


class CollectionListForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ["name", "slug", "position", "archive"]

    name = forms.CharField(disabled=True)
    slug = forms.CharField(disabled=True)
    archive = forms.ModelChoiceField(
        queryset=Archive.objects_in_site.all(),
        widget=forms.Select(attrs={"class": "ui fluid dropdown"}),
        required=False,
    )


CollectionFormSet = forms.modelformset_factory(
    Collection, form=CollectionListForm, extra=0, can_delete=False
)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug", "description", "position"]

    description = forms.CharField(required=False, widget=forms.Textarea())


class CategoryListForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug", "position"]

    name = forms.CharField(disabled=True)
    slug = forms.CharField(disabled=True)


CategoryFormSet = forms.modelformset_factory(
    Category, form=CategoryListForm, extra=0, can_delete=False
)


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["name", "slug", "description", "position"]

    description = forms.CharField(required=False, widget=forms.Textarea())


class PersonListForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["name", "slug", "position"]

    name = forms.CharField(disabled=True)
    slug = forms.CharField(disabled=True)


PersonFormSet = forms.modelformset_factory(
    Person, form=PersonListForm, extra=0, can_delete=False
)


class KeywordForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = ["name", "slug", "description", "position"]

    description = forms.CharField(required=False, widget=forms.Textarea())


class KeywordListForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = ["name", "slug", "position"]

    name = forms.CharField(disabled=True)
    slug = forms.CharField(disabled=True)


KeywordFormSet = forms.modelformset_factory(
    Keyword, form=KeywordListForm, extra=0, can_delete=False
)


CollectionFormField = forms.ModelChoiceField(
    queryset=Collection.objects_in_site.all(),
    widget=forms.Select(attrs={"class": "ui fluid dropdown"}),
    required=True,
)


class PieceForm(forms.ModelForm):
    class Meta:
        model = Piece
        fields = [
            "collection",
            "is_published",
            "code",
            "title",
            "kind",
            "thumb",
            "categories",
            "people",
            "keywords",
        ]

    thumb = forms.ImageField(widget=ImageFileInput())
    kind = forms.ChoiceField(
        choices=PieceConstants.KIND_CHOICES,
        widget=forms.Select(attrs={"class": "ui fluid dropdown"}),
        required=True,
    )
    collection = CollectionFormField
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects_in_site.all(),
        widget=forms.SelectMultiple(attrs={"class": "ui fluid dropdown"}),
        required=False,
    )
    people = forms.ModelMultipleChoiceField(
        queryset=Person.objects_in_site.all(),
        widget=forms.SelectMultiple(attrs={"class": "ui fluid dropdown"}),
        required=False,
    )
    keywords = forms.ModelMultipleChoiceField(
        queryset=Keyword.objects_in_site.all(),
        widget=forms.SelectMultiple(attrs={"class": "ui fluid dropdown"}),
        required=False,
    )


class PieceListForm(forms.ModelForm):
    class Meta:
        model = Piece
        fields = [
            "code",
            "kind",
            "title",
            "thumb",
            "is_published",
        ]

    code = forms.CharField(disabled=True)
    kind = forms.CharField(disabled=True)
    title = forms.CharField(disabled=True)
    thumb = forms.ImageField(widget=ImageFileInput(), disabled=True)


PieceFormSet = forms.modelformset_factory(
    Piece, form=PieceListForm, extra=0, can_delete=False
)


class PieceMetaForm(forms.ModelForm):
    class Meta:
        model = PieceMeta
        fields = [
            "event",
            "description",
            "description_date",
            "location",
            "duration",
            "register_date",
            "register_author",
            "productor",
            "notes",
            "archivist_notes",
            "documentary_unit",
            "lang",
            "original_format",
        ]
