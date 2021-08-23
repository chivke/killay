from django.views.generic import DetailView

from cmpirque.videos.models import Video


class VideoMixin:
    model = Video
    slug_field = "code"


class VideoDetailView(VideoMixin, DetailView):
    pass


video_detail_view = VideoDetailView.as_view()
