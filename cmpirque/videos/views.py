from django.contrib.auth.mixins import AccessMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)


from cmpirque.videos.forms import VideoForm, VideoMetaForm
from cmpirque.videos.models import Video


class VideoMixin:
    model = Video
    slug_field = "code"


class AdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if (
            not request.user.is_authenticated
            or not request.user.is_superuser
        ):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class VideoAdminMixin(VideoMixin, AdminRequiredMixin):
    form_class = VideoForm
    meta_form_class = VideoMetaForm

    def get_meta_form(self):
        kwargs = super().get_form_kwargs()
        if self.object is not None:
            kwargs["instance"] = self.object.meta
        return self.meta_form_class(**kwargs)

    def validate_forms(self):
        form = self.get_form()
        meta_form = self.get_meta_form()
        if form.is_valid() and meta_form.is_valid():
            return self.form_valid(form, meta_form)
        else:
            return self.form_invalid(form, meta_form)

    def form_invalid(self, form, meta_form):
        context = self.get_context_data(form=form)
        context["meta_form"] = meta_form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        metaform_kwargs = (
            {"instance": self.object.meta}
            if hasattr(self, "object")
            and getattr(self, "object") is not None
            else {}
        )
        context["meta_form"] = self.meta_form_class(**metaform_kwargs)
        return context


class VideoDetailView(VideoMixin, DetailView):
    pass


video_detail_view = VideoDetailView.as_view()


class VideoDeleteView(VideoAdminMixin, DeleteView):
    success_url = reverse_lazy('home')


video_delete_view = VideoDeleteView.as_view()


class VideoCreateView(VideoAdminMixin, CreateView):
    def post(self, request, *args, **kwargs):
        self.object = None
        return self.validate_forms()

    def form_valid(self, form, meta_form):
        form.instance.meta = meta_form.save()
        self.object = form.save()
        return super().form_valid(form)


video_create_view = VideoCreateView.as_view()


class VideoUpdateView(VideoAdminMixin, UpdateView):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.validate_forms()

    def form_valid(self, form, meta_form):
        self.object.meta = meta_form.save()
        self.object = form.save()
        return super().form_valid(form)


video_update_view = VideoUpdateView.as_view()
