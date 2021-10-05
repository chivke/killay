from django import forms


from killay.videos.models import (
    Video,
    VideoCategory,
    VideoCategorization,
    VideoCollection,
    VideoKeyword,
    VideoMeta,
    VideoPerson,
    VideoProvider,
    VideoSequence,
)

from killay.admin.utils import ImageFileInput


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["code", "is_visible", "thumb"]

    thumb = forms.ImageField(widget=ImageFileInput(), required=False)


class VideoMetaForm(forms.ModelForm):
    class Meta:
        model = VideoMeta
        fields = "__all__"

    register_date = forms.DateField(
        widget=forms.TextInput(attrs={"type": "date"}), required=False
    )


class VideoProviderForm(forms.ModelForm):
    class Meta:
        model = VideoProvider
        fields = ["active", "ply_embed_id", "plyr_provider"]


VideoProviderFormSet = forms.inlineformset_factory(
    Video, VideoProvider, form=VideoProviderForm, extra=1
)


class VideoSequenceForm(forms.ModelForm):
    class Meta:
        model = VideoSequence
        fields = ["title", "content", "ini", "end"]

    content = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 2}))


VideoSequenceFormSet = forms.modelformset_factory(
    VideoSequence, form=VideoSequenceForm, extra=0, can_delete=True
)


CollectionFormField = forms.ModelChoiceField(
    queryset=VideoCollection.objects.all(),
    widget=forms.Select(attrs={"class": "ui fluid dropdown"}),
    required=True,
)


class VideoCategorizationForm(forms.ModelForm):
    class Meta:
        model = VideoCategorization
        fields = ["collection", "categories", "people", "keywords"]

    collection = CollectionFormField
    categories = forms.ModelMultipleChoiceField(
        queryset=VideoCategory.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "ui fluid dropdown"}),
        required=False,
    )
    people = forms.ModelMultipleChoiceField(
        queryset=VideoPerson.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "ui fluid dropdown"}),
        required=False,
    )
    keywords = forms.ModelMultipleChoiceField(
        queryset=VideoKeyword.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "ui fluid dropdown"}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.set_collection_filter()

    def set_collection_filter(self):
        for field in ["categories", "people", "keywords"]:
            self.fields[field].queryset = self.fields[field].queryset.filter(
                collection_id=self.instance.collection.id
            )


class VideoCollectionForm(forms.ModelForm):
    class Meta:
        model = VideoCollection
        fields = ["name", "slug", "description", "position"]

    description = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"rows": 1})
    )


VideoCollectionFormSet = forms.modelformset_factory(
    VideoCollection, form=VideoCollectionForm, extra=1, can_delete=True
)


class VideoCategoryForm(forms.ModelForm):
    class Meta:
        model = VideoCategory
        fields = ["name", "slug", "description", "collection", "position", "collection"]

    collection = CollectionFormField


class VideoCategoryQuickForm(VideoCategoryForm):
    class Meta:
        fields = ["name", "slug", "collection", "position", "collection"]


VideoCategoryFormSet = forms.modelformset_factory(
    VideoCategory, form=VideoCategoryQuickForm, extra=1, can_delete=True
)


class VideoPersonForm(forms.ModelForm):
    class Meta:
        model = VideoPerson
        fields = ["name", "slug", "description", "position", "collection"]

    collection = CollectionFormField


class VideoPersonQuickForm(VideoPersonForm):
    class Meta:
        fields = ["name", "slug", "collection", "position", "collection"]


VideoPeopleFormSet = forms.modelformset_factory(
    VideoPerson, form=VideoPersonQuickForm, extra=1, can_delete=True
)


class VideoKeywordForm(forms.ModelForm):
    class Meta:
        model = VideoKeyword
        fields = ["name", "slug", "description", "position", "collection"]

    collection = CollectionFormField


class VideoKeywordQuickForm(forms.ModelForm):
    class Meta:
        model = VideoKeyword
        fields = ["name", "slug", "position", "collection"]

    collection = CollectionFormField


VideoKeywordFormSet = forms.modelformset_factory(
    VideoKeyword, form=VideoKeywordQuickForm, extra=1, can_delete=True
)
