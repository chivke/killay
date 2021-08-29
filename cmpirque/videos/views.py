from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView
from django.urls import reverse


from cmpirque.videos.models import Video, VideoCategory, VideoKeyword, VideoPerson

from cmpirque.admin.mixins import PublishRequiredMixin


class VideoMixin(PublishRequiredMixin):
    model = Video
    slug_field = "code"


class VideoDetailView(VideoMixin, DetailView):
    queryset = Video.objects.filter(is_visible=True)


video_detail_view = VideoDetailView.as_view()


class VideoListView(PublishRequiredMixin, ListView):
    model = Video
    paginate_by = 50


video_list_view = VideoListView.as_view()


class CategorizationMixin(PublishRequiredMixin):
    paginate_by = 50

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        video_categorizations = self.object.videos.all()
        context["page_obj"] = self.get_page_obj(video_categorizations)
        return context

    def get_page_obj(self, video_categorizations):
        videos = Video.objects.filter(
            id__in=video_categorizations.values_list("video_id", flat=True)
        )
        paginator = Paginator(videos, self.paginate_by)
        return paginator.get_page(self.request.GET.get("page"))


class VideoCategoryDetailView(CategorizationMixin, DetailView):
    model = VideoCategory
    slug_field = "slug"


video_category_list_view = VideoCategoryDetailView.as_view()


class VideoPersonDetailView(CategorizationMixin, DetailView):
    model = VideoPerson
    slug_field = "slug"


video_person_list_view = VideoPersonDetailView.as_view()


class VideoKeywordDetailView(CategorizationMixin, DetailView):
    model = VideoKeyword
    slug_field = "slug"


video_keyword_list_view = VideoKeywordDetailView.as_view()


class VideoSearchView(PublishRequiredMixin, ListView):
    paginate_by = 50

    def get_queryset(self):
        return Video.objects.filter(
            Q(code__icontains=self.query_search)
            | Q(meta__title__icontains=self.query_search)
            | Q(meta__description__icontains=self.query_search)
        )

    def get(self, request, *args, **kwargs):
        self.query_search = self.request.GET.get("q")
        if not self.query_search:
            return HttpResponseRedirect(reverse("videos:list"))
        return super().get(request, *args, **kwargs)


video_search_list_view = VideoSearchView.as_view()
