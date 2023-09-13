from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext

from killay.admin.lib.constants import LogoConstants
from killay.admin.models import Logo, SiteConfiguration, SocialMedia
from killay.admin.utils import ImageFileInput
from killay.archives.lib.constants import (
    ArchiveConstants,
    CategoryConstants,
    CollectionConstants,
    KeywordConstants,
    PersonConstants,
    PieceConstants,
    PieceMetaConstants,
    PlaceConstants,
    PlaceAddressConstants,
    ProviderConstants,
    SequenceConstants,
)
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
from killay.pages.lib.constants import PageConstants
from killay.pages.models import Page
from killay.viewer.lib.constants import ViewerConstants
from killay.viewer.models import Viewer


class SiteConfigurationForm(forms.ModelForm):
    class Meta:
        model = SiteConfiguration
        fields = [
            "name",
            "domain",
            "is_published",
            "footer_is_visible",
        ]


class ViewerForm(forms.ModelForm):
    class Meta:
        model = Viewer
        fields = [
            "scope",
            "scope_archive",
            "scope_collection",
            "home",
            "home_page",
        ]

    scope = forms.ChoiceField(
        choices=ViewerConstants.SCOPE_CHOICES,
        widget=forms.Select(attrs={"class": "ui fluid dropdown"}),
        required=True,
        help_text=ViewerConstants.HELP_TEXT_SCOPE,
    )
    scope_archive = forms.ModelChoiceField(
        queryset=Archive.objects_in_site.all(),
        widget=forms.Select(attrs={"class": "ui fluid dropdown"}),
        required=False,
        help_text=ViewerConstants.HELP_TEXT_SCOPE_ARCHIVE,
    )
    scope_collection = forms.ModelChoiceField(
        queryset=Collection.objects_in_site.all(),
        widget=forms.Select(attrs={"class": "ui fluid dropdown"}),
        required=False,
        help_text=ViewerConstants.HELP_TEXT_SCOPE_COLLECTION,
    )
    home = forms.ChoiceField(
        choices=ViewerConstants.HOME_CHOICES,
        widget=forms.Select(attrs={"class": "ui fluid dropdown"}),
        help_text=ViewerConstants.HELP_TEXT_HOME,
        required=True,
    )
    home_page = forms.ModelChoiceField(
        queryset=Page.objects_in_site.all(),
        widget=forms.Select(attrs={"class": "ui fluid dropdown"}),
        help_text=ViewerConstants.HELP_TEXT_HOME_PAGE,
        required=False,
    )

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        scope = cleaned_data.get("scope")
        if scope == ViewerConstants.SCOPE_ONE_ARCHIVE and not cleaned_data.get(
            "scope_archive"
        ):
            raise ValidationError(
                {"scope_archive": ViewerConstants.ERROR_SCOPE_ONE_ARCHIVE}
            )

        if scope == ViewerConstants.SCOPE_ONE_COLLECTION and not cleaned_data.get(
            "scope_collection"
        ):
            raise ValidationError(
                {"scope_collection": ViewerConstants.ERROR_SCOPE_ONE_COLLECTION}
            )


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

    image = forms.ImageField(
        widget=ImageFileInput(),
        help_text=LogoConstants.FIELD_IMAGE_HELP_TEXT,
    )


LogoFormSet = forms.modelformset_factory(Logo, form=LogoForm, extra=0, can_delete=True)


class ArchiveForm(forms.ModelForm):
    class Meta:
        model = Archive
        fields = [
            "name",
            "slug",
            "is_visible",
            "is_restricted",
            "places",
            "description",
            "position",
        ]

    description = forms.CharField(
        help_text=ArchiveConstants.FIELD_DESCRIPTION_HELP_TEXT,
        required=False,
        widget=forms.Textarea(),
    )
    places = forms.ModelMultipleChoiceField(
        label=ArchiveConstants.FIELD_PLACES,
        help_text=ArchiveConstants.FIELD_PLACES_HELP_TEXT,
        queryset=Place.objects_in_site.all(),
        widget=forms.SelectMultiple(attrs={"class": "ui fluid dropdown"}),
        required=False,
    )


class ArchiveListForm(forms.ModelForm):
    class Meta:
        model = Archive
        fields = ["name", "slug", "description", "position"]

    name = forms.CharField(
        help_text=ArchiveConstants.FIELD_NAME_HELP_TEXT,
        disabled=True,
    )
    slug = forms.CharField(
        help_text=ArchiveConstants.FIELD_SLUG_HELP_TEXT, disabled=True
    )
    description = forms.CharField(
        help_text=ArchiveConstants.FIELD_DESCRIPTION_HELP_TEXT, disabled=True
    )


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
            "is_visible",
            "is_restricted",
            "places",
            "description",
            "position",
        ]

    archive = forms.ModelChoiceField(
        help_text=CollectionConstants.FIELD_ARCHIVE_HELP_TEXT,
        queryset=Archive.objects_in_site.all(),
        widget=forms.Select(attrs={"class": "ui fluid dropdown"}),
        required=True,
    )
    places = forms.ModelMultipleChoiceField(
        help_text=CollectionConstants.FIELD_PLACES_HELP_TEXT,
        queryset=Place.objects_in_site.all(),
        widget=forms.SelectMultiple(attrs={"class": "ui fluid dropdown"}),
        required=False,
    )
    name = forms.CharField(
        label=CollectionConstants.FIELD_NAME,
        help_text=CollectionConstants.FIELD_NAME_HELP_TEXT,
    )
    slug = forms.SlugField(
        label=CollectionConstants.FIELD_SLUG,
        help_text=CollectionConstants.FIELD_SLUG_HELP_TEXT,
    )
    description = forms.CharField(
        label=CollectionConstants.FIELD_DESCRIPTION,
        help_text=CollectionConstants.FIELD_DESCRIPTION_HELP_TEXT,
        widget=forms.Textarea(),
        required=False,
    )
    position = forms.IntegerField(
        label=CollectionConstants.FIELD_POSITION,
        help_text=CollectionConstants.FIELD_POSITION_HELP_TEXT,
    )


class CollectionListForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ["name", "slug", "position", "archive"]

    name = forms.CharField(
        help_text=CollectionConstants.FIELD_NAME_HELP_TEXT, disabled=True
    )
    slug = forms.CharField(
        help_text=CollectionConstants.FIELD_SLUG_HELP_TEXT, disabled=True
    )
    archive = forms.ModelChoiceField(
        queryset=Archive.objects_in_site.all(),
        help_text=CollectionConstants.FIELD_ARCHIVE_HELP_TEXT,
        widget=forms.Select(attrs={"class": "ui fluid dropdown"}),
        required=False,
    )
    position = forms.IntegerField(
        label=CollectionConstants.FIELD_POSITION,
        help_text=CollectionConstants.FIELD_POSITION_HELP_TEXT,
    )


CollectionFormSet = forms.modelformset_factory(
    Collection, form=CollectionListForm, extra=0, can_delete=False
)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug", "collection", "description", "position"]

    name = forms.CharField(
        label=CategoryConstants.FIELD_NAME,
        help_text=CategoryConstants.FIELD_NAME_HELP_TEXT,
    )
    slug = forms.SlugField(
        label=CategoryConstants.FIELD_SLUG,
        help_text=CategoryConstants.FIELD_SLUG_HELP_TEXT,
    )
    description = forms.CharField(
        label=CategoryConstants.FIELD_DESCRIPTION,
        help_text=CategoryConstants.FIELD_DESCRIPTION_HELP_TEXT,
        widget=forms.Textarea(),
        required=False,
    )
    position = forms.IntegerField(
        label=CategoryConstants.FIELD_POSITION,
        help_text=CategoryConstants.FIELD_POSITION_HELP_TEXT,
    )
    collection = forms.ModelChoiceField(
        label=CategoryConstants.FIELD_COLLECTION,
        help_text=CategoryConstants.FIELD_COLLECTION_HELP_TEXT,
        queryset=Collection.objects_in_site.all(),
        widget=forms.Select(attrs={"class": "ui fluid dropdown"}),
        required=True,
    )


class CategoryListForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug", "position", "collection"]

    name = forms.CharField(
        help_text=CategoryConstants.FIELD_NAME_HELP_TEXT, disabled=True
    )
    slug = forms.CharField(
        help_text=CategoryConstants.FIELD_SLUG_HELP_TEXT, disabled=True
    )
    position = forms.IntegerField(
        label=CategoryConstants.FIELD_POSITION,
        help_text=CategoryConstants.FIELD_POSITION_HELP_TEXT,
    )
    collection = forms.ModelChoiceField(
        label=CategoryConstants.FIELD_COLLECTION,
        help_text=CategoryConstants.FIELD_COLLECTION_HELP_TEXT,
        queryset=Collection.objects_in_site.all(),
        widget=forms.Select(attrs={"class": "ui fluid dropdown"}),
        required=True,
    )


CategoryFormSet = forms.modelformset_factory(
    Category, form=CategoryListForm, extra=0, can_delete=False
)


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["name", "slug", "description", "position"]

    name = forms.CharField(
        label=PersonConstants.FIELD_NAME,
        help_text=PersonConstants.FIELD_NAME_HELP_TEXT,
    )
    slug = forms.SlugField(
        label=PersonConstants.FIELD_SLUG,
        help_text=PersonConstants.FIELD_SLUG_HELP_TEXT,
    )
    description = forms.CharField(
        label=PersonConstants.FIELD_DESCRIPTION,
        help_text=PersonConstants.FIELD_DESCRIPTION_HELP_TEXT,
        widget=forms.Textarea(),
        required=False,
    )
    position = forms.IntegerField(
        label=PersonConstants.FIELD_POSITION,
        help_text=PersonConstants.FIELD_POSITION_HELP_TEXT,
    )


class PersonListForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["name", "slug", "position"]

    name = forms.CharField(
        help_text=PersonConstants.FIELD_NAME_HELP_TEXT, disabled=True
    )
    slug = forms.CharField(
        help_text=PersonConstants.FIELD_SLUG_HELP_TEXT, disabled=True
    )
    position = forms.IntegerField(
        label=PersonConstants.FIELD_POSITION,
        help_text=PersonConstants.FIELD_POSITION_HELP_TEXT,
    )


PersonFormSet = forms.modelformset_factory(
    Person, form=PersonListForm, extra=0, can_delete=False
)


class KeywordForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = ["name", "slug", "description", "position"]

    name = forms.CharField(
        label=KeywordConstants.FIELD_NAME,
        help_text=KeywordConstants.FIELD_NAME_HELP_TEXT,
    )
    slug = forms.SlugField(
        label=KeywordConstants.FIELD_SLUG,
        help_text=KeywordConstants.FIELD_SLUG_HELP_TEXT,
    )
    description = forms.CharField(
        label=KeywordConstants.FIELD_DESCRIPTION,
        help_text=KeywordConstants.FIELD_DESCRIPTION_HELP_TEXT,
        widget=forms.Textarea(),
        required=False,
    )
    position = forms.IntegerField(
        label=KeywordConstants.FIELD_POSITION,
        help_text=KeywordConstants.FIELD_POSITION_HELP_TEXT,
    )


class KeywordListForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = ["name", "slug", "position"]

    name = forms.CharField(
        help_text=KeywordConstants.FIELD_NAME_HELP_TEXT, disabled=True
    )
    slug = forms.CharField(
        help_text=KeywordConstants.FIELD_SLUG_HELP_TEXT, disabled=True
    )
    position = forms.IntegerField(
        label=KeywordConstants.FIELD_POSITION,
        help_text=KeywordConstants.FIELD_POSITION_HELP_TEXT,
    )


KeywordFormSet = forms.modelformset_factory(
    Keyword, form=KeywordListForm, extra=0, can_delete=False
)


class PieceForm(forms.ModelForm):
    class Meta:
        model = Piece
        fields = [
            "code",
            "collection",
            "kind",
            "title",
            "thumb",
            "is_published",
            "is_restricted",
            "places",
            "categories",
            "people",
            "keywords",
        ]

    places = forms.ModelMultipleChoiceField(
        label=PieceConstants.FIELD_PLACES,
        help_text=PieceConstants.FIELD_PLACES_HELP_TEXT,
        queryset=Place.objects_in_site.all(),
        widget=forms.SelectMultiple(attrs={"class": "ui fluid dropdown"}),
        required=False,
    )
    thumb = forms.ImageField(
        label=PieceConstants.FIELD_THUMB,
        help_text=PieceConstants.FIELD_THUMB_HELP_TEXT,
        widget=ImageFileInput(),
        required=False,
    )
    kind = forms.ChoiceField(
        label=PieceConstants.FIELD_KIND,
        help_text=PieceConstants.FIELD_KIND_HELP_TEXT,
        choices=PieceConstants.KIND_CHOICES,
        widget=forms.Select(attrs={"class": "ui fluid dropdown"}),
        required=True,
    )
    collection = forms.ModelChoiceField(
        label=PieceConstants.FIELD_COLLECTION,
        help_text=PieceConstants.FIELD_COLLECTION_HELP_TEXT,
        queryset=Collection.objects_in_site.all(),
        widget=forms.Select(attrs={"class": "ui fluid dropdown"}),
        required=True,
    )
    categories = forms.ModelMultipleChoiceField(
        label=PieceConstants.FIELD_CATEGORIES,
        help_text=PieceConstants.FIELD_CATEGORIES_HELP_TEXT,
        queryset=Category.objects_in_site.all(),
        widget=forms.SelectMultiple(attrs={"class": "ui fluid dropdown"}),
        required=False,
    )
    people = forms.ModelMultipleChoiceField(
        label=PieceConstants.FIELD_PEOPLE,
        help_text=PieceConstants.FIELD_PEOPLE_HELP_TEXT,
        queryset=Person.objects_in_site.all(),
        widget=forms.SelectMultiple(attrs={"class": "ui fluid dropdown"}),
        required=False,
    )
    keywords = forms.ModelMultipleChoiceField(
        label=PieceConstants.FIELD_KEYWORDS,
        help_text=PieceConstants.FIELD_KEYWORDS_HELP_TEXT,
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

    code = forms.CharField(
        label=PieceConstants.FIELD_CODE,
        help_text=PieceConstants.FIELD_CODE_HELP_TEXT,
        disabled=True,
    )
    kind = forms.CharField(
        label=PieceConstants.FIELD_KIND,
        help_text=PieceConstants.FIELD_KIND_HELP_TEXT,
        disabled=True,
    )
    title = forms.CharField(
        label=PieceConstants.FIELD_TITLE,
        help_text=PieceConstants.FIELD_TITLE_HELP_TEXT,
        disabled=True,
    )
    thumb = forms.ImageField(
        label=PieceConstants.FIELD_THUMB,
        help_text=PieceConstants.FIELD_THUMB_HELP_TEXT,
        widget=ImageFileInput(),
        disabled=True,
    )


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
        widget=forms.TextInput(attrs={"type": "date"}),
        help_text=PieceMetaConstants.FIELD_REGISTER_DATE_HELP_TEXT,
        required=False,
    )


class SequenceForm(forms.ModelForm):
    class Meta:
        model = Sequence
        fields = ["title", "content", "ini", "end", "piece"]
        widgets = {"piece": forms.HiddenInput()}

    content = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 4}),
        help_text=SequenceConstants.FIELD_CONTENT_HELP_TEXT,
    )

    def clean(self, *args, **kwargs):
        validated_data = super().clean(*args, **kwargs)
        self._clean_ini_greater_then_end()
        return validated_data

    def _clean_ini_greater_then_end(self):
        ini = self.cleaned_data["ini"]
        end = self.cleaned_data["end"]
        if ini and end and ini >= end:
            raise ValidationError({"ini": "init of sequence must be greater then end"})


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
        help_text=ProviderConstants.FIELD_PLYR_PROVIDER_HELP_TEXT,
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

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        file = cleaned_data.get("file")
        if not file:
            return cleaned_data
        extension = file.name[-3:]
        if extension.lower() not in self.file_extensions:
            raise ValidationError(gettext(f"File must be {self.file_extensions}"))
        return cleaned_data


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
    form.Meta.fields = [
        field for field in form.Meta.fields if field not in ["image", "file"]
    ]
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
        help_text=PlaceConstants.FIELD_ALLOWED_ARCHIVES_HELP_TEXT,
    )
    allowed_collections = forms.ModelMultipleChoiceField(
        queryset=Collection.objects_in_site.all(),
        widget=forms.SelectMultiple(attrs={"class": "ui fluid dropdown"}),
        help_text=PlaceConstants.FIELD_ALLOWED_COLLECTIONS_HELP_TEXT,
        required=False,
    )
    allowed_pieces = forms.ModelMultipleChoiceField(
        queryset=Piece.objects_in_site.all(),
        widget=forms.SelectMultiple(attrs={"class": "ui fluid dropdown"}),
        help_text=PlaceConstants.FIELD_ALLOWED_PIECES_HELP_TEXT,
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
        help_text=PlaceAddressConstants.FIELD_IPV4_HELP_TEXT,
    )


PlaceAddressFormSet = forms.modelformset_factory(
    PlaceAddress, form=PlaceAddressForm, extra=0, can_delete=True
)


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
            "archive",
            "collection",
            "place",
        ]

    kind = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "ui fluid dropdown"}),
        required=True,
        choices=PageConstants.KIND_CHOICES,
        help_text=PageConstants.FIELD_KIND_HELP_TEXT,
    )
    header_image = forms.ImageField(
        help_text=PageConstants.FIELD_HEADER_IMAGE_HELP_TEXT,
        widget=ImageFileInput(),
        required=False,
    )


class PageListForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = [
            "title",
            "slug",
            "kind",
            "is_visible",
            "is_visible_in_navbar",
            "is_visible_in_footer",
            "position",
        ]

    title = forms.CharField(
        disabled=True, help_text=PageConstants.FIELD_TITLE_HELP_TEXT
    )
    slug = forms.CharField(disabled=True, help_text=PageConstants.FIELD_SLUG_HELP_TEXT)
    kind = forms.CharField(disabled=True, help_text=PageConstants.FIELD_KIND_HELP_TEXT)


PageFormSet = forms.modelformset_factory(
    Page, form=PageListForm, extra=0, can_delete=False
)
