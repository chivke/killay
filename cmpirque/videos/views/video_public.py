from django.views.generic import DetailView, ListView

from cmpirque.videos.models import Video


class VideoMixin:
    model = Video
    slug_field = "code"


class VideoDetailView(VideoMixin, DetailView):
    pass


video_detail_view = VideoDetailView.as_view()


class VideoListView(ListView):
    model = Video
    paginate_by = 50


video_list_view = VideoListView.as_view()
