from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.utils.translation import gettext

from cmpirque.admin.mixins import AdminRequiredMixin

from cmpirque.videos.forms import (
    VideoForm,
    VideoMetaForm,
    VideoCategorizationForm,
    VideoCategoryFormSet,
    VideoKeywordFormSet,
    VideoPeopleFormSet,
    VideoProviderFormSet,
    VideoSequenceFormSet,
)
from cmpirque.videos.models import (
    Video,
    VideoCategorization,
    VideoCategory,
    VideoKeyword,
    VideoPerson,
)


class VideoAdminMixin(AdminRequiredMixin):
    model = Video
    slug_field = "code"
    form_class = VideoForm
    meta_form_class = VideoMetaForm
    providers_formset_class = VideoProviderFormSet

    def get_meta_form(self):
        kwargs = super().get_form_kwargs()
        if self.object is not None:
            kwargs["instance"] = self.object.meta
        return self.meta_form_class(**kwargs)

    def get_providers_formset(self):
        kwargs = super().get_form_kwargs()
        if self.object is not None:
            kwargs["instance"] = self.object
        return self.providers_formset_class(**kwargs)

    def get_success_url(self):
        return reverse("admin:videos_update", kwargs={"slug": self.object.code})

    def validate_forms(self):
        form = self.get_form()
        meta_form = self.get_meta_form()
        providers_formset = self.get_providers_formset()
        if form.is_valid() and meta_form.is_valid() and providers_formset.is_valid():
            return self.form_valid(form, meta_form, providers_formset)
        else:
            return self.form_invalid(form, meta_form, providers_formset)

    def form_invalid(self, form, meta_form, providers_formset):
        context = self.get_context_data(form=form)
        context["meta_form"] = meta_form
        context["providers_formset"] = providers_formset
        messages.error(self.request, gettext("Error saving Video"))
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        has_video = hasattr(self, "object") and getattr(self, "object") is not None
        context["meta_form"] = self.meta_form_class(
            **{"instance": self.object.meta} if has_video else {}
        )
        context["providers_formset"] = self.providers_formset_class(
            **{"instance": self.object} if has_video else {}
        )
        return context


class VideoDeleteView(VideoAdminMixin, DeleteView):
    success_url = reverse_lazy("home")
    template_name = "admin/videos/video_delete.html"


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


class VideoSequenceList(AdminRequiredMixin, UpdateView):
    model = Video
    slug_field = "code"
    fields = ["code"]
    template_name_suffix = "_sequences_list"
    formset_class = VideoSequenceFormSet
    template_name = "admin/videos/video_sequences_list.html"

    def get_success_url(self):
        return reverse("admin:videos_sequences_list", kwargs={"slug": self.object.code})

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return {**context, "formset": self.get_formset(), **kwargs}

    def get_formset(self, **kwargs):
        return self.formset_class(**kwargs, instance=self.object)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            return self.formset_valid(formset)
        else:
            return self.formset_invalid(formset)

    def formset_valid(self, formset):
        formset.save()
        messages.info(self.request, gettext("Video sequences saved successfully"))
        return HttpResponseRedirect(self.get_success_url())

    def formset_invalid(self, formset):
        context = self.get_context_data(formset=formset)
        messages.error(self.request, gettext("Error saving video sequences"))
        return self.render_to_response(context)


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


class FormSetListMixin(AdminRequiredMixin, ListView):
    paginate_by = 50
    model = None
    formset_class = None
    label_plural = None
    reverse_url = None
    formset_title = None
    template_name = "admin/formset_list.html"

    def get_context_data(self, **kwargs):
        kwargs["total_of_objects"] = self.total_of_objects
        kwargs["formset_title"] = self.formset_title
        kwargs["label_plural"] = self.label_plural
        kwargs["query_search"] = self.query_search
        context = super().get_context_data()
        if "formset" not in kwargs:
            kwargs["formset"] = self.formset_class(queryset=self.object_list)
        return {**context, **kwargs}

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        formset = self.formset_class(queryset=self.object_list, data=request.POST)
        if formset.is_valid():
            return self.formset_valid(formset)
        else:
            return self.formset_invalid(formset)

    def get_queryset(self):
        self.query_search = self.request.GET.get("q") or self.request.POST.get(
            "query_search"
        )
        queryset = (
            self.model.objects.all()
            if not self.query_search
            else self.model.objects.filter(name__icontains=self.query_search)
        )
        self.total_of_objects = queryset.count()
        return queryset

    def get_success_url(self):
        url = reverse(self.reverse_url) + "?"
        if self.query_search:
            url += f"q={self.query_search}"
        page_number = self.request.POST.get("page_number")
        if str(page_number).isnumeric():
            if url[-1] != "?":
                url += "&"
            url += f"page={page_number}"
        return url

    def formset_valid(self, formset):
        self.object_list = formset.save()
        messages.info(
            self.request, gettext(f"Video {self.label_plural} saved successfully")
        )
        return HttpResponseRedirect(self.get_success_url())

    def formset_invalid(self, formset):
        context = self.get_context_data(formset=formset)
        messages.error(self.request, gettext(f"Error saving video {self.label_plural}"))
        return self.render_to_response(context)


class VideoCategoryListView(FormSetListMixin):
    model = VideoCategory
    formset_class = VideoCategoryFormSet
    label_plural = gettext("categories")
    reverse_url = "admin:videos_categories"
    formset_title = gettext("Video Categories")


video_categories_view = VideoCategoryListView.as_view()


class VideoPeopleList(FormSetListMixin):
    model = VideoPerson
    formset_class = VideoPeopleFormSet
    label_plural = gettext("people")
    reverse_url = "admin:videos_people"
    formset_title = gettext("Video People")


video_people_view = VideoPeopleList.as_view()


class VideoKeywordList(FormSetListMixin):
    model = VideoKeyword
    formset_class = VideoKeywordFormSet
    label_plural = gettext("keywords")
    reverse_url = "admin:videos_keywords"
    formset_title = gettext("Video Keywords")


video_keywords_view = VideoKeywordList.as_view()
