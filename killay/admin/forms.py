from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext

from killay.admin.models import Logo, SiteConfiguration, SocialMedia
from killay.admin.utils import ImageFileInput
from killay.archives.lib.constants import PieceConstants, ProviderConstants
from killay.archives.models import (
    Archive,
    Category,
    Collection,
    Keyword,
    Person,
    Piece,
    PieceMeta,
    Provider,
    Sequence,
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

    register_date = forms.DateField(
        widget=forms.TextInput(attrs={"type": "date"}), required=False
    )


class SequenceForm(forms.ModelForm):
    class Meta:
        model = Sequence
        fields = ["title", "content", "ini", "end", "piece"]
        widgets = {"piece": forms.HiddenInput()}

    content = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 4}))

    def clean(self, *args, **kwargs):
        validated_data = super().clean(*args, **kwargs)
        self._clean_ini_greater_then_end()
        return validated_data

    def _clean_ini_greater_then_end(self):
        ini = self.cleaned_data["ini"]
        end = self.cleaned_data["end"]
        if ini and end and ini >= end:
            raise ValidationError("init of sequence must be greater then end")


SequenceFormSet = forms.modelformset_factory(
    Sequence, form=SequenceForm, extra=0, can_delete=True
)


class VideoProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = [
            "piece",
            "active",
            "ply_embed_id",
            "plyr_provider",
        ]
        widgets = {"piece": forms.HiddenInput()}

    plyr_provider = forms.ChoiceField(
        choices=ProviderConstants.PLYR_PROVIDER_CHOICES,
        widget=forms.Select(attrs={"class": "ui fluid dropdown"}),
        required=True,
    )


class ImageProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = [
            "piece",
            "active",
            "image",
        ]
        widgets = {"piece": forms.HiddenInput()}


class FileProviderForm(forms.ModelForm):
    file_extensions = ["mp3", "ogg"]

    class Meta:
        model = Provider
        fields = [
            "piece",
            "active",
            "file",
        ]
        widgets = {"piece": forms.HiddenInput()}

    def clean_file(self):
        data = self.cleaned_data["file"]
        extension = data.name[-3:]
        if extension.lower() not in self.file_extensions:
            raise ValidationError(gettext(f"File must be {self.file_extensions}"))
        return data


class DocumentProviderForm(FileProviderForm):
    file_extensions = ["pdf"]


def get_provider_form_by_piece_kind(
    kind: str, formset: bool = False, **kwargs
) -> forms.ModelForm:
    form = None
    if kind == PieceConstants.KIND_VIDEO:
        form = VideoProviderForm
    elif kind == PieceConstants.KIND_IMAGE:
        form = ImageProviderForm
    elif kind == PieceConstants.KIND_SOUND:
        form = FileProviderForm
    elif kind == PieceConstants.KIND_DOCUMENT:
        form = DocumentProviderForm
    if not formset:
        return form
    return forms.modelformset_factory(
        Provider,
        form=form,
        extra=kwargs.get("extra", 0),
        can_delete=kwargs.get("can_delete", False),
    )


ProviderFormSet = forms.modelformset_factory(
    Provider, form=VideoProviderForm, extra=0, can_delete=True
)

ProviderForm = VideoProviderForm
