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
    Place,
    PlaceAddress,
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
        fields = ["config", "provider", "url", "is_visible", "position"]
        widgets = {"config": forms.HiddenInput()}


SocialMediaFormSet = forms.modelformset_factory(
    SocialMedia, form=SocialMediaForm, extra=0
)


class LogoForm(forms.ModelForm):
    class Meta:
        model = Logo
        fields = ["configuration", "name", "image", "is_visible", "position"]
        widgets = {"configuration": forms.HiddenInput()}

    image = forms.ImageField(widget=ImageFileInput())


LogoFormSet = forms.modelformset_factory(Logo, form=LogoForm, extra=0, can_delete=True)


class ArchiveForm(forms.ModelForm):
    class Meta:
        model = Archive
        fields = ["name", "slug", "places", "description", "position"]

    description = forms.CharField(required=False, widget=forms.Textarea())
    places = forms.ModelMultipleChoiceField(
        queryset=Place.objects_in_site.all(),
        widget=forms.SelectMultiple(attrs={"class": "ui fluid dropdown"}),
        required=False,
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
        fields = [
            "archive",
            "name",
            "slug",
            "is_restricted",
            "places",
            "description",
            "position",
        ]

    archive = forms.ModelChoiceField(
        queryset=Archive.objects_in_site.all(),
        widget=forms.Select(attrs={"class": "ui fluid dropdown"}),
        required=False,
    )
    places = forms.ModelMultipleChoiceField(
        queryset=Place.objects_in_site.all(),
        widget=forms.SelectMultiple(attrs={"class": "ui fluid dropdown"}),
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
        fields = ["name", "slug", "collection", "description", "position"]

    description = forms.CharField(required=False, widget=forms.Textarea())
    collection = forms.ModelChoiceField(
        queryset=Collection.objects_in_site.all(),
        widget=forms.Select(attrs={"class": "ui fluid dropdown"}),
        required=False,
    )


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


class PieceForm(forms.ModelForm):
    class Meta:
        model = Piece
        fields = [
            "collection",
            "is_published",
            "is_restricted",
            "places",
            "code",
            "title",
            "kind",
            "thumb",
            "categories",
            "people",
            "keywords",
        ]

    places = forms.ModelMultipleChoiceField(
        queryset=Place.objects_in_site.all(),
        widget=forms.SelectMultiple(attrs={"class": "ui fluid dropdown"}),
        required=False,
    )
    thumb = forms.ImageField(widget=ImageFileInput())
    kind = forms.ChoiceField(
        choices=PieceConstants.KIND_CHOICES,
        widget=forms.Select(attrs={"class": "ui fluid dropdown"}),
        required=True,
    )
    collection = forms.ModelChoiceField(
        queryset=Collection.objects_in_site.all(),
        widget=forms.Select(attrs={"class": "ui fluid dropdown"}),
        required=True,
    )
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


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = [
            "name",
            "allowed_collections",
            "allowed_archives",
            "allowed_pieces",
        ]

    allowed_archives = forms.ModelMultipleChoiceField(
        queryset=Archive.objects_in_site.all(),
        widget=forms.SelectMultiple(attrs={"class": "ui fluid dropdown"}),
        required=False,
    )
    allowed_collections = forms.ModelMultipleChoiceField(
        queryset=Collection.objects_in_site.all(),
        widget=forms.SelectMultiple(attrs={"class": "ui fluid dropdown"}),
        required=False,
    )
    allowed_pieces = forms.ModelMultipleChoiceField(
        queryset=Piece.objects_in_site.all(),
        widget=forms.SelectMultiple(attrs={"class": "ui fluid dropdown"}),
        required=False,
    )


PlaceFormSet = forms.modelformset_factory(
    Place, form=PlaceForm, extra=0, can_delete=False
)

IPV4_PATTERN = (
    r"^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$"
)


class PlaceAddressForm(forms.ModelForm):
    class Meta:
        model = PlaceAddress
        fields = ["place", "ipv4", "description"]
        widgets = {"place": forms.HiddenInput()}

    ipv4 = forms.GenericIPAddressField(
        widget=forms.TextInput(
            attrs={
                "pattern": IPV4_PATTERN,
                "minlength": 7,
                "maxlength": 15,
                "size": 15,
                "placeholder": "x.x.x.x",
            }
        ),
        required=True,
    )


PlaceAddressFormSet = forms.modelformset_factory(
    PlaceAddress, form=PlaceAddressForm, extra=0, can_delete=True
)
