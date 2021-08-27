from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

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
        return reverse("videos:update", kwargs={"slug": self.object.code})

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


video_delete_view = VideoDeleteView.as_view()


class VideoCreateView(VideoAdminMixin, CreateView):
    def post(self, request, *args, **kwargs):
        self.object = None
        return self.validate_forms()

    def form_valid(self, form, meta_form, providers_formset):
        form.instance.meta = meta_form.save()
        self.object = form.save()
        return super().form_valid(form)


video_create_view = VideoCreateView.as_view()


class VideoUpdateView(VideoAdminMixin, UpdateView):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.validate_forms()

    def form_valid(self, form, meta_form, providers_formset):
        self.object.meta = meta_form.save()
        self.object = form.save()
        return super().form_valid(form)


video_update_view = VideoUpdateView.as_view()


class VideoSequenceList(AdminRequiredMixin, UpdateView):
    model = Video
    slug_field = "code"
    fields = ["code"]
    template_name_suffix = "_sequences_list"
    formset_class = VideoSequenceFormSet

    def get_success_url(self):
        return reverse("videos:sequences_list", kwargs={"slug": self.object.code})

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
        return HttpResponseRedirect(self.get_success_url())

    def formset_invalid(self, formset):
        context = self.get_context_data(formset=formset)
        return self.render_to_response(context)


video_sequences_list = VideoSequenceList.as_view()


class VideoCategorizationUpdateView(AdminRequiredMixin, UpdateView):
    model = Video
    categorization_model = VideoCategorization
    slug_field = "code"
    template_name_suffix = "_categorization"
    form_class = VideoCategorizationForm

    def get_success_url(self):
        return reverse("videos:categorization", kwargs={"slug": self.object.code})

    def get_object(self):
        instance = super().get_object()
        try:
            instance.categorization
        except VideoCategorization.DoesNotExist:
            instance.categorization = self.categorization_model()
        return instance

    def form_valid(self, form):
        self.object.categorization = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, "object"):
            kwargs.update({"instance": self.object.categorization})
        return kwargs


video_categorization = VideoCategorizationUpdateView.as_view()


class VideoCategoryListView(AdminRequiredMixin, ListView):
    model = VideoCategory

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return {**context, "formset": VideoCategoryFormSet(), **kwargs}

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        formset = VideoCategoryFormSet(data=request.POST)
        if formset.is_valid():
            return self.formset_valid(formset)
        else:
            return self.formset_invalid(formset)

    def formset_valid(self, formset):
        self.object_list = formset.save()
        return HttpResponseRedirect(reverse("videos:categories"))

    def formset_invalid(self, formset):
        context = self.get_context_data(formset=formset)
        return self.render_to_response(context)


video_categories_view = VideoCategoryListView.as_view()


class VideoPeopleList(AdminRequiredMixin, ListView):
    model = VideoPerson

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return {**context, "formset": VideoPeopleFormSet(), **kwargs}

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        formset = VideoPeopleFormSet(data=request.POST)
        if formset.is_valid():
            return self.formset_valid(formset)
        else:
            return self.formset_invalid(formset)

    def formset_valid(self, formset):
        self.object_list = formset.save()
        return HttpResponseRedirect(reverse("videos:people"))

    def formset_invalid(self, formset):
        context = self.get_context_data(formset=formset)
        return self.render_to_response(context)


video_people_view = VideoPeopleList.as_view()


class VideoKeywordList(AdminRequiredMixin, ListView):
    model = VideoKeyword

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return {**context, "formset": VideoKeywordFormSet(), **kwargs}

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        formset = VideoKeywordFormSet(data=request.POST)
        if formset.is_valid():
            return self.formset_valid(formset)
        else:
            return self.formset_invalid(formset)

    def formset_valid(self, formset):
        self.object_list = formset.save()
        return HttpResponseRedirect(reverse("videos:categories"))

    def formset_invalid(self, formset):
        context = self.get_context_data(formset=formset)
        return self.render_to_response(context)


video_keywords_view = VideoKeywordList.as_view()
