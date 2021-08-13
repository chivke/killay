
from django.views.generic import DetailView

from cmpirque.videos.models import Video


class VideoDetailView(DetailView):
    model = Video
    slug_field = "code"
    slug_field_kwarg = "code"


video_detail_view = VideoDetailView.as_view()
