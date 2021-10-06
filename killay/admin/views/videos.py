from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django.utils.translation import gettext, gettext_lazy

from killay.admin.mixins import (
    AdminRequiredMixin,
    AdminDeleteMixin,
    AdminUpdateMixin,
    InlineFormSetMixin,
    VideoAdminMixin,
    FormSetMixin,
)

from killay.videos.forms import (
    VideoCategorizationForm,
    VideoCategoryForm,
    VideoCategoryFormSet,
    VideoCollectionForm,
    VideoCollectionFormSet,
    VideoKeywordForm,
    VideoKeywordFormSet,
    VideoPeopleFormSet,
    VideoPersonForm,
    VideoSequenceForm,
    VideoSequenceFormSet,
)
from killay.videos.models import (
    Video,
    VideoCategorization,
    VideoCategory,
    VideoCollection,
    VideoKeyword,
    VideoPerson,
    VideoSequence,
)


class GetVideoAsObjectMixin:
    def get_object(self):
        collection = self.kwargs.get("collection")
        code = self.kwargs.get("slug")

        try:
            obj = self.model.objects.get(
                code=code, categorization__collection__slug=collection
            )
        except self.model.DoesNotExist:
            raise Http404(gettext("Video not exists"))
        return obj


class VideoDeleteView(GetVideoAsObjectMixin, AdminDeleteMixin):
    model = Video
    slug_field = "code"
    reverse_success_url = "admin:configuration"


video_delete_view = VideoDeleteView.as_view()


class VideoCreateView(VideoAdminMixin, CreateView):
    template_name = "admin/videos/video_form.html"

    def post(self, request, *args, **kwargs):
        self.object = None
        return self.validate_forms()

    def form_valid(self, form, meta_form, categorization_form, providers_formset):
        form.instance.meta = meta_form.save()
        self.object = form.save()
        categorization_form.instance.video = self.object
        categorization_form.save()
        providers_formset.instance = self.object
        providers_formset.save()
        messages.info(
            self.request, gettext(f"Video [{self.object.code}] saved successfully")
        )
        return super().form_valid(form)


video_create_view = VideoCreateView.as_view()


class VideoUpdateView(GetVideoAsObjectMixin, VideoAdminMixin, UpdateView):
    template_name = "admin/videos/video_form.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.validate_forms()

    def form_valid(self, form, meta_form, categorization_form, providers_formset):
        self.object.meta = meta_form.save()
        self.object.categorization = categorization_form.save()
        self.object = form.save()
        providers_formset.save()
        messages.info(
            self.request, gettext(f"Video [{self.object.code}] saved successfully")
        )
        return super().form_valid(form)


video_update_view = VideoUpdateView.as_view()


class VideoSequenceList(GetVideoAsObjectMixin, InlineFormSetMixin):
    model = Video
    slug_field = "code"
    inline_model = VideoSequence
    inline_field = "video"
    formset_class = VideoSequenceFormSet
    search_field = "content"
    reverse_url = "admin:videos_sequences_list"
    title = gettext_lazy("Video Sequences")
    create_reverse_link = "admin:videos_sequences_create"
    compact_fields = ["content"]


video_sequences_list_view = VideoSequenceList.as_view()


class VideoSequenceCreateView(GetVideoAsObjectMixin, AdminRequiredMixin, CreateView):
    model = Video
    inline_model = VideoSequence
    form_class = VideoSequenceForm
    template_name = "admin/generic_form.html"
    extra_context = {"form_title": gettext_lazy("Create Video Sequence")}

    def get(self, request, *args, **kwargs):
        self.video = self.get_video()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.video = self.get_video()
        return super().post(request, *args, **kwargs)

    def get_video(self):
        return super().get_object()
        try:
            video = self.model.objects.get(code=self.kwargs.get("slug"))
        except self.model.DoesNotExist:
            raise Http404(gettext("Video not found"))
        return video

    def form_valid(self, form):
        form.instance.video = self.video
        self.object = form.save()
        return super().form_valid(form)

    def get_queryset(self):
        queryset = self.inline_model.filter(video=self.video)
        return queryset

    def get_success_url(self):
        messages.info(
            self.request, gettext(f'Video Sequence "{self.object.title}" was created')
        )
        return reverse(
            "admin:videos_sequences_list",
            kwargs={
                "collection": self.video.categorization.collection.slug,
                "slug": self.video.code,
            },
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["object"] = self.video
        return context


video_sequences_create_view = VideoSequenceCreateView.as_view()


class VideoCategorizationUpdateView(
    GetVideoAsObjectMixin, AdminRequiredMixin, UpdateView
):
    model = Video
    categorization_model = VideoCategorization
    slug_field = "code"
    template_name_suffix = "_categorization"
    form_class = VideoCategorizationForm
    template_name = "admin/videos/video_categorization.html"

    def get_object(self):
        instance = super().get_object()
        try:
            instance.categorization
        except VideoCategorization.DoesNotExist:
            instance.categorization = self.categorization_model()
        return instance

    def form_valid(self, form):
        self.object.categorization = form.save()
        messages.info(self.request, gettext("Video categorization saved successfully"))
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, "object"):
            kwargs.update({"instance": self.object.categorization})
        return kwargs

    def form_invalid(self, *args, **kwargs):
        messages.error(self.request, gettext("Error saving video categorization"))
        return super().form_invalid(*args, **kwargs)


video_categorization_view = VideoCategorizationUpdateView.as_view()


class VideoCollectionListView(FormSetMixin):
    model = VideoCollection
    formset_class = VideoCollectionFormSet
    reverse_url = "admin:videos_collections"
    title = gettext("Video Collections")
    create_reverse_link = "admin:videos_collection_create"


video_collections_view = VideoCollectionListView.as_view()


class VideoCollectionCreateView(AdminRequiredMixin, CreateView):
    form_class = VideoCollectionForm
    template_name = "admin/generic_form.html"
    extra_context = {"form_title": gettext_lazy("Create Collection")}

    def get_success_url(self):
        messages.info(self.request, gettext(f'Collection "{self.object}" was created'))
        return reverse(
            "admin:videos_collection_update", kwargs={"slug": self.object.slug}
        )


video_collection_create_view = VideoCollectionCreateView.as_view()


class VideoCollectionUpdateView(AdminUpdateMixin):
    model = VideoCollection
    form_class = VideoCollectionForm
    reverse_success_url = "admin:videos_collection_update"


video_collection_update_view = VideoCollectionUpdateView.as_view()


class VideoCategoryListView(FormSetMixin):
    model = VideoCategory
    formset_class = VideoCategoryFormSet
    reverse_url = "admin:videos_categories"
    title = gettext("Video Categories")
    create_reverse_link = "admin:videos_category_create"


video_categories_view = VideoCategoryListView.as_view()


class VideoCategoryCreateView(AdminRequiredMixin, CreateView):
    form_class = VideoCategoryForm
    template_name = "admin/generic_form.html"
    extra_context = {"form_title": gettext_lazy("Create Category")}

    def get_success_url(self):
        messages.info(self.request, gettext(f'Category "{self.object}" was created'))
        return reverse(
            "admin:videos_category_update", kwargs={"slug": self.object.slug}
        )


video_category_create_view = VideoCategoryCreateView.as_view()


class VideoCategoryUpdateView(AdminUpdateMixin):
    model = VideoCategory
    form_class = VideoCategoryForm
    reverse_success_url = "admin:videos_category_update"

    def get_object(self):
        kwargs = {
            "slug": self.kwargs.get("slug"),
            "collection__slug": self.kwargs.get("collection"),
        }
        try:
            obj = self.model.objects.get(**kwargs)
        except self.model.DoesNotExist:
            raise Http404()
        return obj


video_category_update_view = VideoCategoryUpdateView.as_view()


class VideoPeopleList(FormSetMixin):
    model = VideoPerson
    formset_class = VideoPeopleFormSet
    reverse_url = "admin:videos_people"
    title = gettext("Video People")
    create_reverse_link = "admin:videos_person_create"


video_people_view = VideoPeopleList.as_view()


class VideoPersonCreateView(AdminRequiredMixin, CreateView):
    form_class = VideoPersonForm
    template_name = "admin/generic_form.html"
    extra_context = {"form_title": gettext_lazy("Create Person")}

    def get_success_url(self):
        messages.info(self.request, gettext(f'Person "{self.object}" was created'))
        return reverse("admin:videos_person_update", kwargs={"slug": self.object.slug})


video_person_create_view = VideoPersonCreateView.as_view()


class VideoPersonUpdateView(VideoCategoryUpdateView):
    model = VideoPerson
    form_class = VideoPersonForm
    reverse_success_url = "admin:videos_person_update"


video_person_update_view = VideoPersonUpdateView.as_view()


class VideoKeywordList(FormSetMixin):
    model = VideoKeyword
    formset_class = VideoKeywordFormSet
    reverse_url = "admin:videos_keywords"
    title = gettext("Video Keywords")
    create_reverse_link = "admin:videos_keyword_create"


video_keywords_view = VideoKeywordList.as_view()


class VideoKeywordCreateView(AdminRequiredMixin, CreateView):
    form_class = VideoKeywordForm
    template_name = "admin/generic_form.html"
    extra_context = {"form_title": gettext_lazy("Create Keyword")}

    def get_success_url(self):
        messages.info(self.request, gettext(f'Keyword "{self.object}" was created'))
        return reverse("admin:videos_keyword_update", kwargs={"slug": self.object.slug})


video_keyword_create_view = VideoKeywordCreateView.as_view()


class VideoKeywordUpdateView(VideoCategoryUpdateView):
    model = VideoKeyword
    form_class = VideoKeywordForm
    reverse_success_url = "admin:videos_keyword_update"


video_keyword_update_view = VideoKeywordUpdateView.as_view()
