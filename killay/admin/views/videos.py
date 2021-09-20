from django.contrib import messages
from django.http import HttpResponseRedirect
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


class VideoDeleteView(AdminDeleteMixin):
    model = Video
    slug_field = "code"
    reverse_success_url = "admin:configuration"


video_delete_view = VideoDeleteView.as_view()


class VideoCreateView(VideoAdminMixin, CreateView):
    template_name = "admin/videos/video_form.html"

    def post(self, request, *args, **kwargs):
        self.object = None
        return self.validate_forms()

    def form_valid(self, form, meta_form, providers_formset):
        form.instance.meta = meta_form.save()
        self.object = form.save()
        providers_formset.instance = self.object
        providers_formset.save()
        messages.info(
            self.request, gettext(f"Video [{self.object.code}] saved successfully")
        )
        return super().form_valid(form)


video_create_view = VideoCreateView.as_view()


class VideoUpdateView(VideoAdminMixin, UpdateView):
    template_name = "admin/videos/video_form.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.validate_forms()

    def form_valid(self, form, meta_form, providers_formset):
        self.object.meta = meta_form.save()
        self.object = form.save()
        providers_formset.save()
        messages.info(
            self.request, gettext(f"Video [{self.object.code}] saved successfully")
        )
        return super().form_valid(form)


video_update_view = VideoUpdateView.as_view()


class VideoSequenceList(InlineFormSetMixin):
    model = Video
    slug_field = "code"
    inline_model = VideoSequence
    inline_field = "video"
    formset_class = VideoSequenceFormSet
    search_field = "content"
    reverse_url = "admin:videos_sequences_list"
    title = gettext_lazy("Video Sequences")


video_sequences_list = VideoSequenceList.as_view()


class VideoCategorizationUpdateView(AdminRequiredMixin, UpdateView):
    model = Video
    categorization_model = VideoCategorization
    slug_field = "code"
    template_name_suffix = "_categorization"
    form_class = VideoCategorizationForm
    template_name = "admin/videos/video_categorization.html"

    def get_success_url(self):
        return reverse("admin:videos_categorization", kwargs={"slug": self.object.code})

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


video_categorization = VideoCategorizationUpdateView.as_view()


class VideoCollectionListView(FormSetMixin):
    model = VideoCollection
    formset_class = VideoCollectionFormSet
    reverse_url = "admin:videos_collections"
    title = gettext("Video Collections")


video_collections_view = VideoCollectionListView.as_view()


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


video_categories_view = VideoCategoryListView.as_view()


class VideoCategoryUpdateView(AdminUpdateMixin):
    model = VideoCategory
    form_class = VideoCategoryForm
    reverse_success_url = "admin:videos_category_update"


video_category_update_view = VideoCategoryUpdateView.as_view()


class VideoPeopleList(FormSetMixin):
    model = VideoPerson
    formset_class = VideoPeopleFormSet
    reverse_url = "admin:videos_people"
    title = gettext("Video People")


video_people_view = VideoPeopleList.as_view()


class VideoPersonUpdateView(AdminUpdateMixin):
    model = VideoPerson
    form_class = VideoPersonForm
    reverse_success_url = "admin:videos_person_update"


video_person_update_view = VideoPersonUpdateView.as_view()


class VideoKeywordList(FormSetMixin):
    model = VideoKeyword
    formset_class = VideoKeywordFormSet
    reverse_url = "admin:videos_keywords"
    title = gettext("Video Keywords")


video_keywords_view = VideoKeywordList.as_view()


class VideoKeywordUpdateView(AdminUpdateMixin):
    model = VideoKeyword
    form_class = VideoKeywordForm
    reverse_success_url = "admin:videos_keyword_update"


video_keyword_update_view = VideoKeywordUpdateView.as_view()
