
from django.forms import ModelForm

from cmpirque.videos.models import Video, VideoMeta


class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ["code", "is_visible", "thumb"]


class VideoMetaForm(ModelForm):
    class Meta:
        model = VideoMeta
        fields = "__all__"
