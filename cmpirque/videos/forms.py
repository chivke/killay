from django import forms


from cmpirque.videos.models import (
    Video,
    VideoCategory,
    VideoCategorization,
    VideoKeyword,
    VideoMeta,
    VideoPerson,
    VideoProvider,
    VideoSequence,
)


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["code", "is_visible", "thumb"]


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


VideoSequenceFormSet = forms.inlineformset_factory(
    Video, VideoSequence, form=VideoSequenceForm, extra=1
)


class VideoCategorizationForm(forms.ModelForm):
    class Meta:
        model = VideoCategorization
        fields = ["categories", "people", "keywords"]

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


class VideoCategoryForm(forms.ModelForm):
    class Meta:
        model = VideoCategory
        fields = ["name", "slug", "description", "position"]

    description = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"rows": 1})
    )


VideoCategoryFormSet = forms.modelformset_factory(
    VideoCategory, form=VideoCategoryForm, extra=1, can_delete=True
)


class VideoPersonForm(forms.ModelForm):
    class Meta:
        model = VideoPerson
        fields = ["name", "slug", "description", "position"]

    description = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"rows": 1})
    )


VideoPeopleFormSet = forms.modelformset_factory(
    VideoPerson, form=VideoPersonForm, extra=1, can_delete=True
)


class VideoKeywordForm(forms.ModelForm):
    class Meta:
        model = VideoKeyword
        fields = ["name", "slug", "description", "position"]

    description = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"rows": 1})
    )


VideoKeywordFormSet = forms.modelformset_factory(
    VideoKeyword, form=VideoKeywordForm, extra=1, can_delete=True
)
