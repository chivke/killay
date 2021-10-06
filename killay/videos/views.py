from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.views.generic import DetailView, ListView
from django.views.generic.list import MultipleObjectMixin
from django.urls import reverse
from django.utils.translation import gettext


from killay.videos.models import (
    Video,
    VideoCategory,
    VideoCollection,
    VideoKeyword,
    VideoPerson,
)

from killay.admin.mixins import PublishRequiredMixin


class VideoMixin(PublishRequiredMixin):
    model = Video
    slug_field = "code"


class VideoDetailView(VideoMixin, DetailView):
    def get_object(self):
        kwargs = {
            "code": self.kwargs.get("slug"),
            "categorization__collection__slug": self.kwargs.get("collection"),
        }
        if not self.request.user.is_authenticated:
            kwargs["is_visible"] = True
        try:
            obj = self.model.objects.get(**kwargs)
        except self.model.DoesNotExist:
            raise Http404(gettext("Not video found"))
        return obj


video_detail_view = VideoDetailView.as_view()


class CategorizationMixin(PublishRequiredMixin, MultipleObjectMixin):
    paginate_by = 54
    template_name = "videos/video_filtered_list.html"
    slug_field = "slug"

    def get_context_data(self, *args, **kwargs):
        self.object_list = self.get_videos_queryset()
        context = super().get_context_data(*args, **kwargs)
        context.update(self.get_pagination_context())
        return context

    def get_pagination_context(self):
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            self.object_list, self.paginate_by
        )
        return {"paginator": paginator, "page_obj": page, "is_paginated": is_paginated}

    def get_videos_queryset(self):
        queryset = (
            self.object.videos.filter(video__is_visible=True)
            if not self.request.user.is_authenticated
            else self.object.videos.all()
        )
        self.query_search = self.request.GET.get("q")
        if self.query_search:
            queryset = queryset.filter(
                Q(video__code__icontains=self.query_search)
                | Q(video__meta__title__icontains=self.query_search)
                | Q(video__meta__description__icontains=self.query_search)
            )
        self.total_of_videos = queryset.count()
        return Video.objects.filter(categorization__in=queryset)

    def get_object(self):
        kwargs = {
            "slug": self.kwargs.get("slug"),
            "collection__slug": self.kwargs.get("collection"),
        }
        if not self.request.user.is_authenticated:
            kwargs["collection__is_visible"] = True
        try:
            obj = self.model.objects.get(**kwargs)
        except self.model.DoesNotExist:
            raise Http404(gettext("Not video found"))
        return obj


class VideoCollectionView(CategorizationMixin, DetailView):
    model = VideoCollection
    template_name = "videos/video_filtered_list.html"

    def get_object(self):
        kwargs = {"slug": self.kwargs.get("slug")}
        if not self.request.user.is_authenticated:
            kwargs["is_visible"] = True
        try:
            obj = self.model.objects.get(**kwargs)
        except self.model.DoesNotExist:
            raise Http404(gettext("Not collection found"))
        return obj


video_collection_list_view = VideoCollectionView.as_view()


class VideoCategoryDetailView(CategorizationMixin, DetailView):
    model = VideoCategory


video_category_list_view = VideoCategoryDetailView.as_view()


class VideoPersonDetailView(CategorizationMixin, DetailView):
    model = VideoPerson


video_person_list_view = VideoPersonDetailView.as_view()


class VideoKeywordDetailView(CategorizationMixin, DetailView):
    model = VideoKeyword


video_keyword_list_view = VideoKeywordDetailView.as_view()


class VideoSearchView(PublishRequiredMixin, ListView):
    paginate_by = 54

    def get_queryset(self):
        return Video.objects.filter(
            Q(code__icontains=self.query_search)
            | Q(meta__title__icontains=self.query_search)
            | Q(meta__description__icontains=self.query_search)
        )

    def render_to_response(self, context):
        context["query_search"] = self.query_search
        if not self.object_list:
            messages.info(
                self.request, gettext(f'Videos with "{self.query_search}" not founded.')
            )
        return super().render_to_response(context)

    def get(self, request, *args, **kwargs):
        self.query_search = self.request.GET.get("q")
        if not self.query_search:
            return HttpResponseRedirect(reverse("home"))
        return super().get(request, *args, **kwargs)


video_search_list_view = VideoSearchView.as_view()
